import './SignalCards.css';

const AGENT_META = {
  sentinel: { name: 'Sentinel', icon: '🛡️', color: '#e74c3c' },
  scout: { name: 'Scout', icon: '🔭', color: '#2ecc71' },
  historian: { name: 'Historian', icon: '📚', color: '#3498db' },
  mirror: { name: 'Mirror', icon: '🪞', color: '#9b59b6' },
};

const QUALITY_CONFIG = {
  HIGH: { color: '#2ecc71', label: 'HIGH', bg: 'rgba(46,204,113,0.12)' },
  MEDIUM: { color: '#f39c12', label: 'MED', bg: 'rgba(243,156,18,0.12)' },
  LOW: { color: '#e74c3c', label: 'LOW', bg: 'rgba(231,76,60,0.12)' },
};

export default function SignalCards({ compressionMap }) {
  if (!compressionMap) return null;

  return (
    <div className="signal-cards-container">
      <div className="signal-cards-title">Signal Quality</div>
      <div className="signal-cards-subtitle">How calibrated each instinct is for this decision</div>
      <div className="signal-cards">
        {Object.entries(AGENT_META).map(([key, meta]) => {
          const data = compressionMap[key];
          if (!data) return null;
          const quality = QUALITY_CONFIG[data.quality] || QUALITY_CONFIG.MEDIUM;
          return (
            <div
              key={key}
              className="signal-card"
              style={{ borderLeftColor: meta.color }}
            >
              <div className="signal-card-header">
                <span className="signal-icon">{meta.icon}</span>
                <span className="signal-name">{meta.name}</span>
                <span
                  className="signal-quality-badge"
                  style={{ color: quality.color, background: quality.bg }}
                >
                  {quality.label}
                </span>
              </div>
              <div className="signal-text">{data.signal}</div>
              <div className="signal-weight-bar">
                <div
                  className="signal-weight-fill"
                  style={{
                    width: `${Math.round((data.weight ?? 0) * 100)}%`,
                    background: meta.color,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
