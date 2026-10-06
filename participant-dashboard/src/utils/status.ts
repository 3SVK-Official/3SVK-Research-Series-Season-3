// Maps every status string used across submissions/repository/credentials
// to a shared badge style. Centralised so new statuses only need one edit.
export const statusClass: Record<string, string> = {
  Submitted: 'status submitted',
  Evaluated: 'status evaluated',
  Pending: 'status pending',
  Uncompleted: 'status uncompleted',
  Verified: 'status evaluated',
  Failed: 'status failed',
  Passed: 'status evaluated',
};
