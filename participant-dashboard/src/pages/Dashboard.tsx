import { Award, CheckCircle2, Clock3, FileCheck2, Github } from 'lucide-react';
import { Badge } from '../components/dashboard/Badge';
import { Milestone } from '../components/dashboard/Milestone';
import { Panel } from '../components/dashboard/Panel';
import { BadgeCardSkeleton, MilestoneSkeleton, RepoStatusSkeleton, StatSkeleton } from '../components/dashboard/Skeletons';
import { Stat } from '../components/dashboard/Stat';
import { participant } from '../data/mockData';
import { useDashboardSnapshot } from '../hooks/useDashboardSnapshot';
import { statusClass } from '../utils/status';

export function Dashboard({ progress, completed }: { progress: number; completed: number }) {
  const { loading, snapshot } = useDashboardSnapshot();

  return (
    <>
      <section className="hero">
        <div>
          <p className="eyebrow">Participant workspace</p>
          <h1>Welcome back, {participant.name.split(' ')[0]}.</h1>
          <p className="muted">
            Track your research-series milestones, repository verification, and credentials from one place.
          </p>
        </div>
        <div className="hero-id">
          <span>Participant ID</span>
          <strong>{participant.participantId}</strong>
        </div>
      </section>

      <div className="stats-grid" aria-busy={loading} aria-label="Dashboard metrics">
        {loading || !snapshot ? (
          <>
            <StatSkeleton />
            <StatSkeleton />
            <StatSkeleton />
            <StatSkeleton />
          </>
        ) : (
          <>
            <Stat icon={<Clock3 />} label="Participation" value={snapshot.participant.participationStatus} note="Current status" />
            <Stat icon={<FileCheck2 />} label="Milestones" value={`${completed}/${snapshot.milestones.length}`} note={`${progress}% progress`} />
            <Stat icon={<Github />} label="Repository" value={snapshot.repository.status} note={`${snapshot.repository.checksPassed}/${snapshot.repository.checksTotal} checks passed`} />
            <Stat icon={<Award />} label="Credentials" value={`${snapshot.badges.filter((b) => b.earned).length} earned`} note={`${snapshot.badges.length} total milestones`} />
          </>
        )}
      </div>

      <div className="section-grid">
        <Panel title="Submission progress" subtitle="Your current research-series milestones">
          {loading || !snapshot ? (
            <div aria-busy="true" aria-label="Loading submission status">
              <div className="progress-row">
                <span className="skeleton-line skeleton-w-40" />
                <strong className="skeleton-line skeleton-w-20" />
              </div>
              <div className="progress-track">
                <div className="skeleton-fill" style={{ width: '100%' }} />
              </div>
              <div className="timeline">
                <MilestoneSkeleton />
                <MilestoneSkeleton />
                <MilestoneSkeleton />
              </div>
            </div>
          ) : (
            <>
              <div className="progress-row">
                <span>Overall progress</span>
                <strong>{progress}%</strong>
              </div>
              <div className="progress-track">
                <div style={{ width: `${progress}%` }} />
              </div>
              <div className="timeline">
                {snapshot.milestones.map((m) => (
                  <Milestone key={m.id} milestone={m} />
                ))}
              </div>
            </>
          )}
        </Panel>

        <Panel title="Repository verification" subtitle="Latest automated verification snapshot">
          {loading || !snapshot ? (
            <div aria-busy="true" aria-label="Loading repository status">
              <RepoStatusSkeleton />
            </div>
          ) : (
            <>
              <div className="repo-card">
                <div className="repo-icon">
                  <Github size={22} />
                </div>
                <div className="repo-main">
                  <strong>{snapshot.repository.repository}</strong>
                  <span>
                    {snapshot.repository.pullRequest} · {snapshot.repository.branch}
                  </span>
                </div>
                <span className={statusClass[snapshot.repository.status]}>{snapshot.repository.status}</span>
              </div>
              <div className="check-summary">
                <CheckCircle2 size={18} />
                <span>
                  {snapshot.repository.checksPassed} of {snapshot.repository.checksTotal} checks passed
                </span>
                <code>{snapshot.repository.commit}</code>
              </div>
              <div className="detail-line">
                <span>Last checked</span>
                <strong>{snapshot.repository.lastChecked}</strong>
              </div>
            </>
          )}
        </Panel>
      </div>

      <Panel title="Milestone credentials" subtitle="Earned and upcoming recognition">
        {loading || !snapshot ? (
          <div className="badge-grid" aria-busy="true" aria-label="Loading credentials">
            <BadgeCardSkeleton />
            <BadgeCardSkeleton />
            <BadgeCardSkeleton />
          </div>
        ) : (
          <div className="badge-grid">
            {snapshot.badges.map((badge) => (
              <Badge key={badge.id} badge={badge} />
            ))}
          </div>
        )}
      </Panel>
    </>
  );
}
