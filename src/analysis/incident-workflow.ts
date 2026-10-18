export type IncidentStatus = "new" | "investigating" | "resolved";

export interface IncidentStatusChange {
  from: IncidentStatus;
  to: IncidentStatus;
  changedAt: string;
}

export interface IncidentWorkflowState {
  status: IncidentStatus;
  updatedAt: string;
  history: IncidentStatusChange[];
}

const allowedTransitions: Record<IncidentStatus, IncidentStatus[]> = {
  new: ["investigating", "resolved"],
  investigating: ["new", "resolved"],
  resolved: ["investigating"]
};

export class InMemoryIncidentWorkflow {
  private readonly states = new Map<string, IncidentWorkflowState>();

  get(incidentId: string, now = new Date().toISOString()): IncidentWorkflowState {
    const existing = this.states.get(incidentId);
    if (existing) {
      return structuredClone(existing);
    }

    const initial: IncidentWorkflowState = {
      status: "new",
      updatedAt: now,
      history: []
    };
    this.states.set(incidentId, initial);
    return structuredClone(initial);
  }

  transition(
    incidentId: string,
    status: IncidentStatus,
    now = new Date().toISOString()
  ): IncidentWorkflowState | undefined {
    const current = this.states.get(incidentId) ?? {
      status: "new" as const,
      updatedAt: now,
      history: []
    };

    if (current.status === status) {
      this.states.set(incidentId, current);
      return structuredClone(current);
    }
    if (!allowedTransitions[current.status].includes(status)) {
      return undefined;
    }

    const next: IncidentWorkflowState = {
      status,
      updatedAt: now,
      history: [
        ...current.history,
        { from: current.status, to: status, changedAt: now }
      ]
    };
    this.states.set(incidentId, next);
    return structuredClone(next);
  }

  clear(): void {
    this.states.clear();
  }
}

export function isIncidentStatus(value: unknown): value is IncidentStatus {
  return value === "new" || value === "investigating" || value === "resolved";
}
