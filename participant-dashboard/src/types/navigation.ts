// The project has no URL router yet, so navigation is driven by this
// in-memory page state (see App.tsx). Add new sections here and they'll
// be available to Sidebar, Header, and the page switch in App.tsx.
export type Page = 'dashboard' | 'submissions' | 'repository' | 'credentials' | 'profile' | 'settings';

export const pageLabels: Record<Page, string> = {
  dashboard: 'Dashboard',
  submissions: 'Submissions',
  repository: 'Repository Verification',
  credentials: 'Credentials',
  profile: 'Profile',
  settings: 'Settings',
};
