import { Menu, Moon, Search, Sun } from 'lucide-react';
import type { Page } from '../../types/navigation';
import { pageLabels } from '../../types/navigation';

export function Header({
  page,
  dark,
  onToggleDark,
  onOpenMenu,
}: {
  page: Page;
  dark: boolean;
  onToggleDark: () => void;
  onOpenMenu: () => void;
}) {
  return (
    <header className="topbar">
      <button className="icon-button menu-button" onClick={onOpenMenu} aria-label="Open menu">
        <Menu size={20} />
      </button>
      <div className="breadcrumb">
        <span>Participant Portal</span>
        <b>/</b>
        <strong>{pageLabels[page]}</strong>
      </div>
      <div className="top-actions">
        <div className="search">
          <Search size={16} />
          <input placeholder="Search dashboard" aria-label="Search dashboard" />
        </div>
        <button className="icon-button" onClick={onToggleDark} aria-label="Toggle theme">
          {dark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <div className="avatar">AK</div>
      </div>
    </header>
  );
}
