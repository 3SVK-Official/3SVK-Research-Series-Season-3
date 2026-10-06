You are a senior frontend engineer and UI/UX designer. Build a production-quality Participant Dashboard frontend for the 3SVK Research Series Season 3.

CONTEXT
The existing public repository mainly contains the AetherMesh telemetry backend demo. The Participant Dashboard frontend should be developed as a modular frontend that can later connect to live APIs. Do NOT modify or depend on the AetherMesh telemetry UI unless required for integration.

TECH STACK
- React.js with TypeScript
- Prefer Next.js App Router if creating a new app; otherwise integrate cleanly into the existing React/Next project.
- Tailwind CSS
- Component-based architecture
- Mock JSON/TypeScript data only for now
- No hard-coded API calls
- Keep API integration easy to add later
- Responsive desktop/tablet/mobile
- Accessible semantic HTML
- Dark mode + light mode
- Clean enterprise visual language for 3SVK

CORE REQUIREMENTS

1. AUTHENTICATION / PROFILE OVERVIEW
Create a participant dashboard shell with:
- Participant name
- Unique Participant ID
- Registered track(s)
- Profile/avatar area
- Authentication/user menu placeholder
- Current overall participation status
- Responsive sidebar/top navigation

2. SUBMISSION STATUS TRACKER
Create a polished milestone tracker/table showing:
- Phase-1 Registration
- Phase-2 Prototype
- Phase-3 Final Evaluation
Each milestone must support:
- Submitted
- Pending
- Evaluated
- Uncompleted
Show status badges, dates, short descriptions, and optional evaluation/result information.
Make this data-driven from mock data.

3. REPOSITORY VERIFICATION LOGS
Create a repository verification section showing:
- GitHub repository/PR reference
- PR number
- Branch
- Latest commit SHA (shortened in UI)
- Validation timestamp
- Validation status
- Checks passed/failed
- Commit verification history
- Expandable/detail view for individual verification events
Do not implement real GitHub API access yet. Use a clean service/data abstraction so a real endpoint can replace mock data later.

4. MILESTONE / CREDENTIAL BADGES
Create a badge/certificate area with:
- Earned milestone badges
- Locked/upcoming badges
- Completion/certificate indicator
- Badge title
- Description
- Earned date
- Visual distinction between earned and locked
Do not invent real certificates; use clearly marked mock/demo data.

5. DASHBOARD OVERVIEW
Add useful summary cards at the top:
- Participation progress
- Completed milestones
- Repository verification status
- Credentials earned
Use simple visual indicators/progress bars where appropriate.

6. DESIGN
Visual direction:
- Modern
- Minimal
- Enterprise-grade
- Professional research/technology platform
- 3SVK branding
- Strong typography hierarchy
- Generous spacing
- Clean cards
- Subtle borders/shadows
- Dark/light theme
- Responsive navigation
Avoid excessive gradients, flashy animations, glassmorphism, or gaming-style UI.

7. COMPONENT ARCHITECTURE
Use reusable components such as:
- DashboardLayout
- Sidebar
- Header
- ProfileOverview
- SummaryCard
- SubmissionTracker
- SubmissionStatusBadge
- RepositoryVerification
- VerificationLogTable
- VerificationDetails
- BadgeGrid
- CredentialCard
- ThemeToggle
- EmptyState
- LoadingState
- ErrorState

8. DATA ARCHITECTURE
Create typed mock data under src/data/ and types under src/types/.
Example entities:
Participant
SubmissionMilestone
RepositoryVerification
VerificationEvent
CredentialBadge

Keep UI components independent of the exact mock payload. Create a small service/data layer so API calls can later replace mocks without rewriting the UI.

9. UX DETAILS
Include:
- Active navigation state
- Responsive sidebar/mobile navigation
- Search/filter where useful
- Status filtering for submissions
- Repository verification status filtering
- Tooltips for technical values such as commit SHA
- Accessible buttons and keyboard navigation
- Empty/error states
- Consistent date formatting
- No broken links
- No fake claims that data is live

10. ROUTING
At minimum create:
- /dashboard
- /dashboard/submissions
- /dashboard/repository
- /dashboard/credentials
- /dashboard/profile

The dashboard overview may summarize all major sections.

11. MOCK DATA
Use realistic but obviously fictional demo data, e.g.:
Name: Ayesha Khan
Participant ID: 3SVK-P-2026-0142
Tracks: AI Research, Full-Stack Engineering
Do not use real participant information.

12. QUALITY
Before finishing:
- Run TypeScript/type checking
- Run lint
- Run build
- Fix all errors
- Ensure responsive layouts
- Ensure dark/light themes work
- Ensure every navigation item points to a valid page
- Ensure no placeholder "TODO" remains in the visible UI
- Keep comments limited to useful architectural explanations

DELIVERABLE
Return:
1. Complete source code
2. Clear file structure
3. Setup/run instructions
4. List of created pages/components
5. Explanation of where live API integration should be connected later
6. Verification results for typecheck/lint/build

IMPORTANT
Do not over-engineer authentication or backend integration. This task is specifically the Participant Dashboard frontend with mock data and an API-ready architecture.
