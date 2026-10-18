import { useEffect, useState } from 'react';
import { badges, milestones, participant, repository } from '../data/mockData';
import type { CredentialBadge, Participant, RepositoryVerification, SubmissionMilestone } from '../types';

export type DashboardSnapshot = {
  participant: Participant;
  milestones: SubmissionMilestone[];
  repository: RepositoryVerification;
  badges: CredentialBadge[];
};

// Mock data is already in memory, so this resolves immediately.
// Replace the body with a real request when a live dashboard endpoint exists.
export function loadDashboardSnapshot(): Promise<DashboardSnapshot> {
  return Promise.resolve({
    participant,
    milestones,
    repository,
    badges,
  });
}

let cachedSnapshot: DashboardSnapshot | null = null;

export function useDashboardSnapshot() {
  const [snapshot, setSnapshot] = useState<DashboardSnapshot | null>(cachedSnapshot);

  useEffect(() => {
    if (cachedSnapshot) return;

    let cancelled = false;

    loadDashboardSnapshot().then((data) => {
      cachedSnapshot = data;
      if (!cancelled) setSnapshot(data);
    });

    return () => {
      cancelled = true;
    };
  }, []);

  return { loading: snapshot === null, snapshot };
}
