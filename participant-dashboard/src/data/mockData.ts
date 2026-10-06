import type {
  AccountSettings,
  CredentialBadge,
  Participant,
  RepositoryVerification,
  SubmissionMilestone,
} from '../types';

export const participant: Participant = {
  name: 'Rahma Khan',
  participantId: '3SVK-P-2026-0142',
  tracks: ['AI Research', 'Full-Stack Engineering'],
  participationStatus: 'Active Participant',
  email: 'demo.participant@example.com',
};

export const milestones: SubmissionMilestone[] = [
  {
    id: 'm1',
    phase: 'Phase 1',
    title: 'Registration',
    status: 'Submitted',
    date: '2026-09-05',
    description: 'Participant registration and track selection completed.',
  },
  {
    id: 'm2',
    phase: 'Phase 2',
    title: 'Prototype',
    status: 'Evaluated',
    date: '2026-09-18',
    description: 'Prototype submitted and evaluated by the review team.',
    score: 86,
  },
  {
    id: 'm3',
    phase: 'Phase 3',
    title: 'Final Evaluation',
    status: 'Pending',
    date: null,
    description: 'Final evaluation window has not opened yet.',
  },
];

export const repository: RepositoryVerification = {
  repository: '3SVK-Research-Series-Season-3',
  pullRequest: '#42',
  branch: 'feature/participant-dashboard',
  commit: 'a83f9d2c71e8',
  lastChecked: '2026-09-26 14:32 UTC',
  status: 'Verified',
  checksPassed: 8,
  checksTotal: 8,
  events: [
    {
      id: 'v1',
      timestamp: '2026-09-26 14:32 UTC',
      action: 'Repository validation',
      status: 'Passed',
      message: 'Repository and pull request metadata verified.',
    },
    {
      id: 'v2',
      timestamp: '2026-09-26 14:30 UTC',
      action: 'Commit check',
      status: 'Passed',
      message: 'Latest commit is available and reachable from the pull request.',
    },
    {
      id: 'v3',
      timestamp: '2026-09-26 14:29 UTC',
      action: 'Required files',
      status: 'Passed',
      message: 'Expected submission files were detected.',
    },
  ],
};

export const badges: CredentialBadge[] = [
  {
    id: 'b1',
    title: 'Registered Participant',
    description: 'Completed the 3SVK Research Series registration.',
    earned: true,
    earnedDate: '2026-09-05',
  },
  {
    id: 'b2',
    title: 'Prototype Submitted',
    description: 'Submitted a Phase-2 prototype for evaluation.',
    earned: true,
    earnedDate: '2026-09-18',
  },
  {
    id: 'b3',
    title: 'Verified Repository',
    description: 'Repository and submission history passed verification.',
    earned: true,
    earnedDate: '2026-09-26',
  },
  {
    id: 'b4',
    title: 'Finalist',
    description: 'Awarded after the final evaluation stage.',
    earned: false,
  },
  {
    id: 'b5',
    title: 'Completion Credential',
    description: 'Available after all required milestones are completed.',
    earned: false,
  },
];

// Placeholder account preferences. Not persisted anywhere yet — wire this up
// to a real settings/preferences endpoint once one exists.
export const accountSettings: AccountSettings = {
  email: participant.email,
  notifications: [
    {
      id: 'n1',
      label: 'Milestone status changes',
      description: 'Notify me when a submission moves to Evaluated or Pending.',
      enabled: true,
    },
    {
      id: 'n2',
      label: 'Repository verification results',
      description: 'Notify me when a new verification check completes.',
      enabled: true,
    },
    {
      id: 'n3',
      label: 'Credential updates',
      description: 'Notify me when a new badge or credential is earned.',
      enabled: false,
    },
  ],
};
