import { PageIntro } from '../components/dashboard/PageIntro';
import { Panel } from '../components/dashboard/Panel';
import { participant } from '../data/mockData';

export function Profile() {
  return (
    <>
      <PageIntro
        eyebrow="Account"
        title="Participant profile"
        subtitle="Your registration details and selected research tracks."
      />
      <Panel title="Profile overview" subtitle="Demo participant data">
        <div className="profile-card">
          <div className="profile-avatar">AK</div>
          <div className="profile-info">
            <h2>{participant.name}</h2>
            <span>{participant.email}</span>
            <div className="tag-row">
              {participant.tracks.map((t) => (
                <span className="tag" key={t}>
                  {t}
                </span>
              ))}
            </div>
          </div>
          <div className="profile-id">
            <span>Participant ID</span>
            <strong>{participant.participantId}</strong>
          </div>
        </div>
      </Panel>
    </>
  );
}
