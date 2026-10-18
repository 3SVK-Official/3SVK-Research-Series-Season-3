export function StatSkeleton() {
  return (
    <div className="stat stat-skeleton" aria-hidden="true">
      <div className="stat-icon skeleton-fill" />
      <span className="skeleton-line skeleton-w-40" />
      <strong className="skeleton-line skeleton-w-70" />
      <small className="skeleton-line skeleton-w-50" />
    </div>
  );
}

export function MilestoneSkeleton() {
  return (
    <div className="milestone milestone-skeleton" aria-hidden="true">
      <div className="milestone-icon skeleton-fill" />
      <div>
        <strong className="skeleton-line skeleton-w-70" />
        <span className="skeleton-line skeleton-w-90" />
      </div>
      <span className="skeleton-line skeleton-badge" />
    </div>
  );
}

export function BadgeCardSkeleton() {
  return (
    <div className="badge-card badge-card-skeleton" aria-hidden="true">
      <div className="badge-icon skeleton-fill" />
      <div>
        <strong className="skeleton-line skeleton-w-70" />
        <span className="skeleton-line skeleton-w-90" />
        <small className="skeleton-line skeleton-w-40" />
      </div>
    </div>
  );
}

export function RepoStatusSkeleton() {
  return (
    <>
      <div className="repo-card repo-card-skeleton" aria-hidden="true">
        <div className="repo-icon skeleton-fill" />
        <div className="repo-main">
          <strong className="skeleton-line skeleton-w-70" />
          <span className="skeleton-line skeleton-w-50" />
        </div>
        <span className="skeleton-line skeleton-badge" />
      </div>
      <div className="check-summary" aria-hidden="true">
        <span className="skeleton-line skeleton-w-60" />
        <code className="skeleton-line skeleton-w-30" />
      </div>
      <div className="detail-line" aria-hidden="true">
        <span className="skeleton-line skeleton-w-30" />
        <strong className="skeleton-line skeleton-w-40" />
      </div>
    </>
  );
}
