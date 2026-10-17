import {
  Award,
  ChevronDown,
  FileCheck2,
  Github,
  LayoutDashboard,
  Settings as SettingsIcon,
  UserRound,
  X,
} from 'lucide-react';
import { participant } from '../../data/mockData';
import type { Page } from '../../types/navigation';
import { NavItem } from '../dashboard/NavItem';

export function Sidebar({
  page,
  mobileOpen,
  onNavigate,
  onClose,
}: {
  page: Page;
  mobileOpen: boolean;
  onNavigate: (page: Page) => void;
  onClose: () => void;
}) {
  return (
    <aside className={mobileOpen ? 'sidebar open' : 'sidebar'}>
      <div className="brand">
        <div className="brand-mark">3S</div>
        <div>
          <strong>3SVK</strong>
          <span>Research Series · S3</span>
        </div>
        <button className="icon-button mobile-close" onClick={onClose} aria-label="Close menu">
          <X size={18} />
        </button>
      </div>

      <nav>
        <p className="nav-label">Main</p>
        <NavItem icon={<LayoutDashboard size={18} />} label="Dashboard" active={page === 'dashboard'} onClick={() => onNavigate('dashboard')} />
        <NavItem icon={<FileCheck2 size={18} />} label="Submissions" active={page === 'submissions'} onClick={() => onNavigate('submissions')} />
        <NavItem icon={<Github size={18} />} label="Repository Verification" active={page === 'repository'} onClick={() => onNavigate('repository')} />
        <NavItem icon={<Award size={18} />} label="Credentials" active={page === 'credentials'} onClick={() => onNavigate('credentials')} />

        <p className="nav-label profile-label">Account</p>
        <NavItem icon={<UserRound size={18} />} label="Profile" active={page === 'profile'} onClick={() => onNavigate('profile')} />
        <NavItem icon={<SettingsIcon size={18} />} label="Settings" active={page === 'settings'} onClick={() => onNavigate('settings')} />
      </nav>

      <div className="sidebar-footer">
        <div className="mini-avatar">AK</div>
        <div className="mini-user">
          <strong>{participant.name}</strong>
          <span>{participant.participantId}</span>
        </div>
        <ChevronDown size={16} />
      </div>
    </aside>
  );
}
