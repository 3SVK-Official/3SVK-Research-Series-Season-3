import { CheckCircle2, Clock3 } from 'lucide-react';
import type { SubmissionMilestone } from '../../types';
import { statusClass } from '../../utils/status';

export function Milestone({ milestone }: { milestone: SubmissionMilestone }) {
  const isDone = milestone.status === 'Evaluated' || milestone.status === 'Submitted';
  return (
    <div className="milestone">
      <div className={`milestone-icon ${milestone.status.toLowerCase()}`}>
        {isDone ? <CheckCircle2 size={17} /> : <Clock3 size={17} />}
      </div>
      <div>
        <strong>
          {milestone.phase} · {milestone.title}
        </strong>
        <span>{milestone.description}</span>
      </div>
      <span className={statusClass[milestone.status]}>{milestone.status}</span>
    </div>
  );
}
