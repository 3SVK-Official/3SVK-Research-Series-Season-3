import { Award } from 'lucide-react';
import type { CredentialBadge } from '../../types';

export function Badge({ badge }: { badge: CredentialBadge }) {
  return (
    <div className={badge.earned ? 'badge-card' : 'badge-card locked'}>
      <div className="badge-icon">
        <Award size={24} />
      </div>
      <div>
        <strong>{badge.title}</strong>
        <span>{badge.description}</span>
        {badge.earned ? <small>Earned {badge.earnedDate}</small> : <small>Upcoming credential</small>}
      </div>
    </div>
  );
}
