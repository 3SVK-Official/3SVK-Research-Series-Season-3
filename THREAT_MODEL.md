# InfraWeft threat model

**System:** InfraWeft 0.1.0  
**Author:** Snehasish Das  
**Purpose:** Document the risks created by analyzing infrastructure plans and publishing review artifacts.

## 1. System boundary

InfraWeft is a local command-line program. It reads a Terraform plan JSON document, evaluates selected rule conditions and dependency declarations, and writes Markdown or JSON findings. In the current implementation it does not authenticate to a cloud provider, query a live account, call an external model, apply a plan, or stop a deployment.

### Data flow

1. An engineer generates a Terraform plan and converts it to JSON.
2. The plan JSON is read by InfraWeft.
3. The parser extracts changed resources and the configuration dependency graph.
4. Deterministic rules create evidence-linked findings.
5. The scorer assigns triage points.
6. A report may be viewed locally, attached to an internal review, or published.

The plan and resulting report are sensitive inputs/outputs. Local processing reduces external transfer but does not remove local filesystem, log, terminal, backup, or repository risks.

## 2. Assets to protect

| Asset | Security property | Example exposure |
|---|---|---|
| Terraform plan JSON | Confidentiality and integrity | Internal topology, resource names, planned values, and values marked sensitive by Terraform can appear in JSON |
| Generated report | Confidentiality and integrity | Evidence paths and resource names can reveal architecture; evidence values may expose settings |
| Cloud credentials | Confidentiality | Tokens or keys accidentally placed in fixtures, environment dumps, or commits |
| Rule behavior | Integrity and traceability | A code change silently broadens or narrows detection |
| Finding interpretation | Integrity | A reviewer treats a heuristic score as a calibrated probability or safety certificate |
| GitHub submission | Provenance and integrity | A public commit includes production plans or claims not supported by the submitted implementation |

## 3. Trust boundaries

- **Plan-generation boundary:** Terraform and provider plugins produce the plan; InfraWeft does not verify that the plan is current or complete.
- **Filesystem boundary:** the program reads a file supplied by the operator. The operator is responsible for access controls, retention, and cleanup.
- **Parser boundary:** malformed or version-incompatible JSON can cause a rejected input or unhandled edge case. The current tool is not a hardened parser for hostile documents.
- **Interpretation boundary:** the rule set sees selected attributes only. Unknown values, unsupported resource types, organization policy, and effective cloud permissions are outside its current model.
- **Publication boundary:** any report, fixture, screenshot, or log copied to GitHub or the challenge portal crosses from local review into a public or third-party system.

## 4. Threat scenarios and controls

| ID | Scenario | Potential impact | Current or recommended control | Residual risk |
|---|---|---|---|---|
| TM-01 | A real plan JSON is committed to a public repository | Disclosure of internal infrastructure details or sensitive values | Use only synthetic plans in public repository; inspect diffs; maintain ignore rules for real plan artifacts | A developer can still commit a sensitive file or a sanitized file can retain identifiers |
| TM-02 | A reviewer sees no finding and concludes the plan is safe | A risk outside current rules goes unnoticed | Print scope notes; state that no finding is not a safety certification; require normal review and established scanners | Users may ignore caveats or rely on the tool alone |
| TM-03 | A public ingress exception is legitimate but flagged | Unnecessary rework or accidental disruption if remediation is applied blindly | Human disposition, context, owner, expiry, and rollback notes before action | Rules cannot infer business intent |
| TM-04 | Effective IAM access is broader or narrower than the policy snippet suggests | Incorrect severity or missed effective permission | Treat wildcard detection as a signal only; inspect conditions, boundaries, SCPs, and resource policies separately | Current parser does not compute effective permissions |
| TM-05 | Dependency declarations omit an operational dependency | Underestimated blast radius | Explain dependency counts as declared-graph context; compare with architecture/service ownership knowledge | A Terraform graph is not a full runtime dependency graph |
| TM-06 | A malicious or malformed JSON document is supplied | Unexpected parser behavior or resource exhaustion | Use trusted files, constrained execution environments, input-size limits for hosted use, and malformed-input tests | No current claim of adversarial-input hardening |
| TM-07 | An attacker or accidental edit changes a rule without tests | Regression or undetected loss of coverage | Require focused tests, review rule changes, preserve fixtures, and inspect CI results | Existing tests cover only a small synthetic corpus |
| TM-08 | The score is interpreted as breach likelihood | Misallocated remediation effort or false confidence | Label it heuristic and uncalibrated; present rule evidence separately; do not use it as a gate | Numerical scores can still create false precision |
| TM-09 | A generated report is attached to a public pull request | Disclosure of identifiers, addresses, topology, or internal naming | Publish synthetic output only or sanitize and approve a report before sharing | Sanitization can miss contextual identifiers |

## 5. Abuse cases

The following actions must not be supported by project workflow:

- Treating the absence of a finding as authorization to deploy.
- Sending live plan JSON to a public issue, paste site, or repository without review.
- Using the aggregate score as a substitute for backup verification or owner approval.
- Claiming a rule is exhaustive when it only checks selected resource types and attributes.
- Presenting synthetic fixture outputs as production observations or independent benchmarks.

## 6. Operational safeguards

Before analysis:
- Confirm the plan belongs to the intended workspace and revision.
- Generate plan JSON locally in an access-controlled working directory.
- Do not store plan files inside a public project directory.
- Keep cloud credentials out of command output, test fixtures, and environment dumps.

Before publication:
- Inspect `git diff --stat` and `git diff --cached`.
- Search for account IDs, hostnames, IP addresses, access tokens, private endpoints, and secret-like values.
- Publish synthetic fixtures and sanitized reports only.
- Include the actual test command and outcome; do not infer performance from a passing unit test.

## 7. Risk disposition

InfraWeft is a review aid for a restricted set of static signals. It is not a cloud security boundary, policy enforcement point, vulnerability scanner replacement, or deployment approval mechanism. Production use would require broader coverage, security review, version compatibility testing, controlled release practices, and an independently evaluated corpus.
