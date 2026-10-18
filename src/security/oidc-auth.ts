import { randomBytes } from "node:crypto";
import * as oidc from "openid-client";

export type WorkspaceRole = "viewer" | "analyst" | "admin";

export interface AuthenticatedPrincipal {
  subject: string;
  tenantId: string;
  role: WorkspaceRole;
  email?: string;
  displayName?: string;
}

interface Membership {
  tenantId: string;
  role: WorkspaceRole;
}

export interface OidcSettings {
  issuerUrl: URL;
  appBaseUrl: URL;
  clientId: string;
  clientSecret: string;
  tokenAuthMethod: "client_secret_basic" | "client_secret_post";
  memberships: Map<string, Membership>;
}

interface LoginFlow {
  state: string;
  nonce: string;
  codeVerifier: string;
  createdAt: number;
}

interface SessionRecord {
  principal: AuthenticatedPrincipal;
  expiresAt: number;
}

export interface AuthenticationService {
  beginLogin(): Promise<{ flowId: string; authorizationUrl: URL }>;
  completeLogin(callbackUrl: URL, flowId: string | undefined): Promise<{
    sessionId: string;
    principal: AuthenticatedPrincipal;
  } | undefined>;
  getPrincipal(sessionId: string | undefined): AuthenticatedPrincipal | undefined;
  revokeSession(sessionId: string | undefined): void;
  usesSecureCookies(): boolean;
  acceptsOrigin(origin: string | undefined): boolean;
  callbackUrl(search: string): URL;
}

const FLOW_TTL_MS = 10 * 60 * 1000;
const SESSION_TTL_MS = 8 * 60 * 60 * 1000;
const MAX_PENDING_FLOWS = 1000;
const MAX_SESSIONS = 10_000;
const tenantIdPattern = /^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$/;

function parseMemberships(value: string): Map<string, Membership> {
  let parsed: unknown;
  try {
    parsed = JSON.parse(value) as unknown;
  } catch {
    throw new Error("OIDC_MEMBERSHIPS_JSON must be valid JSON.");
  }
  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    throw new Error("OIDC_MEMBERSHIPS_JSON must be an object keyed by identity-provider subject.");
  }

  const memberships = new Map<string, Membership>();
  for (const [subject, entry] of Object.entries(parsed)) {
    if (
      !subject.trim() ||
      typeof entry !== "object" ||
      entry === null ||
      Array.isArray(entry) ||
      Object.keys(entry).length !== 2 ||
      !("tenantId" in entry) ||
      !("role" in entry) ||
      typeof entry.tenantId !== "string" ||
      !tenantIdPattern.test(entry.tenantId) ||
      (entry.role !== "viewer" && entry.role !== "analyst" && entry.role !== "admin")
    ) {
      throw new Error(`OIDC membership for subject "${subject}" is invalid.`);
    }
    memberships.set(subject, { tenantId: entry.tenantId, role: entry.role });
  }
  if (memberships.size === 0) {
    throw new Error("OIDC_MEMBERSHIPS_JSON must contain at least one authorized subject.");
  }
  return memberships;
}

export function readOidcSettings(
  environment: NodeJS.ProcessEnv = process.env
): OidcSettings {
  const issuer = environment.OIDC_ISSUER_URL;
  const clientId = environment.OIDC_CLIENT_ID;
  const clientSecret = environment.OIDC_CLIENT_SECRET;
  const appBase = environment.APP_BASE_URL;
  const rawMemberships = environment.OIDC_MEMBERSHIPS_JSON;
  const tokenAuthMethod = environment.OIDC_TOKEN_AUTH_METHOD ?? "client_secret_basic";
  if (!issuer || !clientId || !clientSecret || !appBase || !rawMemberships) {
    throw new Error(
      "OIDC mode requires OIDC_ISSUER_URL, OIDC_CLIENT_ID, OIDC_CLIENT_SECRET, APP_BASE_URL, and OIDC_MEMBERSHIPS_JSON."
    );
  }

  let issuerUrl: URL;
  let appBaseUrl: URL;
  try {
    issuerUrl = new URL(issuer);
    appBaseUrl = new URL(appBase);
  } catch {
    throw new Error("OIDC_ISSUER_URL and APP_BASE_URL must be valid absolute URLs.");
  }
  const isLocalIssuer = ["localhost", "127.0.0.1", "[::1]"].includes(issuerUrl.hostname);
  const isLocalApp = ["localhost", "127.0.0.1", "[::1]"].includes(appBaseUrl.hostname);
  if (
    (issuerUrl.protocol !== "https:" && !(isLocalIssuer && issuerUrl.protocol === "http:")) ||
    (appBaseUrl.protocol !== "https:" && !(isLocalApp && appBaseUrl.protocol === "http:")) ||
    issuerUrl.username !== "" ||
    issuerUrl.password !== "" ||
    issuerUrl.search !== "" ||
    issuerUrl.hash !== "" ||
    appBaseUrl.username !== "" ||
    appBaseUrl.password !== "" ||
    appBaseUrl.pathname !== "/" ||
    appBaseUrl.search !== "" ||
    appBaseUrl.hash !== ""
  ) {
    throw new Error("OIDC issuer and application URLs must use HTTPS except for loopback development URLs.");
  }
  if (
    !clientId.trim() ||
    !clientSecret.trim() ||
    (tokenAuthMethod !== "client_secret_basic" && tokenAuthMethod !== "client_secret_post")
  ) {
    throw new Error("OIDC client credentials or token authentication method are invalid.");
  }
  if (
    environment.NODE_ENV === "production" &&
    (issuerUrl.protocol !== "https:" || appBaseUrl.protocol !== "https:")
  ) {
    throw new Error("OIDC issuer and APP_BASE_URL must use HTTPS in production.");
  }

  return {
    issuerUrl,
    appBaseUrl,
    clientId,
    clientSecret,
    tokenAuthMethod,
    memberships: parseMemberships(rawMemberships)
  };
}

export class OidcAuthenticator implements AuthenticationService {
  private readonly flows = new Map<string, LoginFlow>();
  private readonly sessions = new Map<string, SessionRecord>();

  private constructor(
    private readonly settings: OidcSettings,
    private readonly configuration: oidc.Configuration
  ) {}

  static async create(
    environment: NodeJS.ProcessEnv = process.env
  ): Promise<OidcAuthenticator> {
    const settings = readOidcSettings(environment);
    const configuration = await oidc.discovery(
      settings.issuerUrl,
      settings.clientId,
      undefined,
      settings.tokenAuthMethod === "client_secret_post"
        ? oidc.ClientSecretPost(settings.clientSecret)
        : oidc.ClientSecretBasic(settings.clientSecret)
    );
    return new OidcAuthenticator(settings, configuration);
  }

  async beginLogin(): Promise<{ flowId: string; authorizationUrl: URL }> {
    const now = Date.now();
    for (const [flowId, flow] of this.flows) {
      if (now - flow.createdAt > FLOW_TTL_MS) this.flows.delete(flowId);
    }
    if (this.flows.size >= MAX_PENDING_FLOWS) {
      throw new Error("Too many pending OIDC sign-in attempts.");
    }

    const flowId = randomBytes(32).toString("base64url");
    const state = oidc.randomState();
    const nonce = oidc.randomNonce();
    const codeVerifier = oidc.randomPKCECodeVerifier();
    const codeChallenge = await oidc.calculatePKCECodeChallenge(codeVerifier);
    this.flows.set(flowId, { state, nonce, codeVerifier, createdAt: now });

    const authorizationUrl = oidc.buildAuthorizationUrl(this.configuration, {
      redirect_uri: new URL("/auth/callback", this.settings.appBaseUrl).href,
      response_type: "code",
      scope: "openid profile email",
      state,
      nonce,
      code_challenge: codeChallenge,
      code_challenge_method: "S256"
    });
    return { flowId, authorizationUrl };
  }

  async completeLogin(callbackUrl: URL, flowId: string | undefined): Promise<{
    sessionId: string;
    principal: AuthenticatedPrincipal;
  } | undefined> {
    if (!flowId) return undefined;
    const flow = this.flows.get(flowId);
    this.flows.delete(flowId);
    if (!flow || Date.now() - flow.createdAt > FLOW_TTL_MS) return undefined;

    const tokens = await oidc.authorizationCodeGrant(
      this.configuration,
      callbackUrl,
      {
        expectedState: flow.state,
        expectedNonce: flow.nonce,
        pkceCodeVerifier: flow.codeVerifier
      }
    );
    const claims = tokens.claims();
    if (!claims || typeof claims.sub !== "string" || !claims.sub.trim()) {
      return undefined;
    }

    const membership = this.settings.memberships.get(claims.sub);
    if (!membership) return undefined;

    const now = Date.now();
    for (const [sessionId, session] of this.sessions) {
      if (now >= session.expiresAt) this.sessions.delete(sessionId);
    }
    if (this.sessions.size >= MAX_SESSIONS) {
      throw new Error("The local OIDC session limit has been reached.");
    }

    const principal: AuthenticatedPrincipal = {
      subject: claims.sub,
      tenantId: membership.tenantId,
      role: membership.role,
      ...(typeof claims.email === "string" ? { email: claims.email } : {}),
      ...(typeof claims.name === "string" ? { displayName: claims.name } : {})
    };
    const sessionId = randomBytes(32).toString("base64url");
    this.sessions.set(sessionId, {
      principal,
      expiresAt: now + SESSION_TTL_MS
    });
    return { sessionId, principal: structuredClone(principal) };
  }

  getPrincipal(sessionId: string | undefined): AuthenticatedPrincipal | undefined {
    if (!sessionId) return undefined;
    const session = this.sessions.get(sessionId);
    if (!session) return undefined;
    if (Date.now() >= session.expiresAt) {
      this.sessions.delete(sessionId);
      return undefined;
    }
    return structuredClone(session.principal);
  }

  revokeSession(sessionId: string | undefined): void {
    if (sessionId) this.sessions.delete(sessionId);
  }

  usesSecureCookies(): boolean {
    return this.settings.appBaseUrl.protocol === "https:";
  }

  callbackUrl(search: string): URL {
    const callback = new URL("/auth/callback", this.settings.appBaseUrl);
    callback.search = search;
    return callback;
  }

  acceptsOrigin(origin: string | undefined): boolean {
    if (!origin) return false;
    try {
      return new URL(origin).origin === this.settings.appBaseUrl.origin;
    } catch {
      return false;
    }
  }
}

export function canReviewIncidents(role: WorkspaceRole): boolean {
  return role === "analyst" || role === "admin";
}

export function canImportEvents(role: WorkspaceRole): boolean {
  return role === "admin";
}
