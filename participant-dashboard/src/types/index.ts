export type SubmissionStatus = 'Submitted' | 'Pending' | 'Evaluated' | 'Uncompleted';

export interface Participant {
  name: string;
  participantId: string;
  tracks: string[];
  participationStatus: string;
  email: string;
}

export interface SubmissionMilestone {
  id: string;
  phase: string;
  title: string;
  status: SubmissionStatus;
  date: string | null;
  description: string;
  score?: number;
}

export interface VerificationEvent {
  id: string;
  timestamp: string;
  action: string;
  status: 'Passed' | 'Failed' | 'Pending';
  message: string;
}

export interface RepositoryVerification {
  repository: string;
  pullRequest: string;
  branch: string;
  commit: string;
  lastChecked: string;
  status: 'Verified' | 'Pending' | 'Failed';
  checksPassed: number;
  checksTotal: number;
  events: VerificationEvent[];
}

export interface CredentialBadge {
  id: string;
  title: string;
  description: string;
  earned: boolean;
  earnedDate?: string;
}

export interface NotificationPreference {
  id: string;
  label: string;
  description: string;
  enabled: boolean;
}

export interface AccountSettings {
  email: string;
  notifications: NotificationPreference[];
}
