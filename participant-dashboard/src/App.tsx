import { useState } from 'react';
import { Header } from './components/layout/Header';
import { Sidebar } from './components/layout/Sidebar';
import { milestones } from './data/mockData';
import { Credentials } from './pages/Credentials';
import { Dashboard } from './pages/Dashboard';
import { Profile } from './pages/Profile';
import { Repository } from './pages/Repository';
import { Settings } from './pages/Settings';
import { Submissions } from './pages/Submissions';
import type { Page } from './types/navigation';

function App() {
  const [page, setPage] = useState<Page>('dashboard');
  const [dark, setDark] = useState(true);
  const [mobileOpen, setMobileOpen] = useState(false);

  const navigate = (next: Page) => {
    setPage(next);
    setMobileOpen(false);
  };

  const completed = milestones.filter((m) => m.status === 'Submitted' || m.status === 'Evaluated').length;
  const progress = Math.round((completed / milestones.length) * 100);

  return (
    <div className={dark ? 'app dark' : 'app'}>
      <Sidebar page={page} mobileOpen={mobileOpen} onNavigate={navigate} onClose={() => setMobileOpen(false)} />

      {mobileOpen && <button className="overlay" onClick={() => setMobileOpen(false)} aria-label="Close navigation" />}

      <main className="main">
        <Header page={page} dark={dark} onToggleDark={() => setDark((d) => !d)} onOpenMenu={() => setMobileOpen(true)} />

        <div className="content">
          {page === 'dashboard' && <Dashboard progress={progress} completed={completed} />}
          {page === 'submissions' && <Submissions />}
          {page === 'repository' && <Repository />}
          {page === 'credentials' && <Credentials />}
          {page === 'profile' && <Profile />}
          {page === 'settings' && <Settings />}
        </div>
      </main>
    </div>
  );
}

export default App;
