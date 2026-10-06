import { useState } from 'react';
import { PageIntro } from '../components/dashboard/PageIntro';
import { Panel } from '../components/dashboard/Panel';
import { accountSettings } from '../data/mockData';

export function Settings() {
  // Local-only UI state. Nothing here is persisted — this is a mock
  // preferences view until a real settings/account endpoint exists.
  const [notifications, setNotifications] = useState(accountSettings.notifications);

  const toggle = (id: string) => {
    setNotifications((prev) => prev.map((n) => (n.id === id ? { ...n, enabled: !n.enabled } : n)));
  };

  return (
    <>
      <PageIntro
        eyebrow="Account"
        title="Settings"
        subtitle="Manage contact details and notification preferences for your participant account."
      />

      <Panel title="Account details" subtitle="Demo data — not yet connected to a live account service">
        <div className="detail-line">
          <span>Contact email</span>
          <strong>{accountSettings.email}</strong>
        </div>
      </Panel>

      <Panel title="Notification preferences" subtitle="Choose what you want to be notified about">
        <div className="settings-list">
          {notifications.map((n) => (
            <div className="settings-row" key={n.id}>
              <div>
                <strong>{n.label}</strong>
                <span>{n.description}</span>
              </div>
              <button
                className={n.enabled ? 'toggle on' : 'toggle'}
                role="switch"
                aria-checked={n.enabled}
                aria-label={n.label}
                onClick={() => toggle(n.id)}
              >
                <span className="toggle-knob" />
              </button>
            </div>
          ))}
        </div>
      </Panel>
    </>
  );
}
