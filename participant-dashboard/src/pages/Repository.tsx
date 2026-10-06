import { CheckCircle2, ExternalLink, Github } from 'lucide-react';
import { PageIntro } from '../components/dashboard/PageIntro';
import { Panel } from '../components/dashboard/Panel';
import { repository } from '../data/mockData';
import { statusClass } from '../utils/status';

export function Repository() {
  return (
    <>
      <PageIntro
        eyebrow="Verification"
        title="Repository verification"
        subtitle="Review the status of your linked repository, pull request, and validation events."
      />
      <div className="repo-detail">
        <Panel title="Linked repository" subtitle="Demo data — ready for API integration">
          <div className="repo-large">
            <div className="repo-icon">
              <Github size={28} />
            </div>
            <div>
              <strong>{repository.repository}</strong>
              <span>
                {repository.pullRequest} · {repository.branch}
              </span>
            </div>
            <button className="secondary">
              <ExternalLink size={16} /> Open PR
            </button>
          </div>
          <div className="repo-meta">
            <div>
              <span>Latest commit</span>
              <code>{repository.commit}</code>
            </div>
            <div>
              <span>Validation status</span>
              <strong className="inline-success">
                <CheckCircle2 size={16} /> {repository.status}
              </strong>
            </div>
            <div>
              <span>Last checked</span>
              <strong>{repository.lastChecked}</strong>
            </div>
          </div>
        </Panel>
        <Panel title="Verification events" subtitle="Most recent validation activity">
          <div className="events">
            {repository.events.map((e) => (
              <div className="event" key={e.id}>
                <div className={`event-dot ${e.status.toLowerCase()}`} />
                <div>
                  <strong>{e.action}</strong>
                  <span>{e.message}</span>
                  <small>{e.timestamp}</small>
                </div>
                <span className={statusClass[e.status]}>{e.status}</span>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </>
  );
}
