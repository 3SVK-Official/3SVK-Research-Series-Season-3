import { Badge } from '../components/dashboard/Badge';
import { PageIntro } from '../components/dashboard/PageIntro';
import { badges } from '../data/mockData';

export function Credentials() {
  return (
    <>
      <PageIntro
        eyebrow="Recognition"
        title="Milestone credentials"
        subtitle="View earned badges and upcoming completion credentials."
      />
      <div className="badge-grid large">
        {badges.map((b) => (
          <Badge key={b.id} badge={b} />
        ))}
      </div>
    </>
  );
}
