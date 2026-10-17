import { useState } from 'react';
import { PageIntro } from '../components/dashboard/PageIntro';
import { milestones } from '../data/mockData';
import { statusClass } from '../utils/status';

const FILTERS = ['All', 'Submitted', 'Evaluated', 'Pending', 'Uncompleted'];

export function Submissions() {
  const [filter, setFilter] = useState('All');
  const visible = filter === 'All' ? milestones : milestones.filter((m) => m.status === filter);

  // Fixed: PageIntro and the fragment below were previously returned as
  // sibling JSX elements with no shared parent. Wrapping everything in a
  // single top-level fragment resolves TS2657 / the Vite parse error.
  return (
    <>
      <PageIntro
        eyebrow="Milestones"
        title="Submission status"
        subtitle="Follow each required submission stage and its evaluation state."
      />

      <div className="filter-row">
        {FILTERS.map((f) => (
          <button key={f} className={filter === f ? 'filter active' : 'filter'} onClick={() => setFilter(f)}>
            {f}
          </button>
        ))}
      </div>

      <div className="table-card">
        <div className="table-head">
          <span>Phase</span>
          <span>Milestone</span>
          <span>Status</span>
          <span>Date</span>
          <span>Result</span>
        </div>
        {visible.map((m) => (
          <div className="table-row" key={m.id}>
            <span className="phase">{m.phase}</span>
            <div>
              <strong>{m.title}</strong>
              <small>{m.description}</small>
            </div>
            <span className={statusClass[m.status]}>{m.status}</span>
            <span>{m.date ?? '—'}</span>
            <span>{m.score ? `${m.score}/100` : '—'}</span>
          </div>
        ))}
      </div>
    </>
  );
}
