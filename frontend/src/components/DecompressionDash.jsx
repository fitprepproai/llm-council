import AgentRadarChart from './RadarChart';
import SignalCards from './SignalCards';
import './DecompressionDash.css';

const AGENT_META = {
  leverage: { name: 'Leverage Hunter', icon: '⚡', color: '#f39c12' },
  position: { name: 'Power Reader', icon: '♟️', color: '#e74c3c' },
  architect: { name: 'The Architect', icon: '🏗️', color: '#3498db' },
  freedom: { name: 'Liberation Auditor', icon: '🔓', color: '#2ecc71' },
};

function LiberationMeter({ score }) {
  if (score == null) return null;
  const pct = Math.round(score * 100);
  const color = pct >= 70 ? '#2ecc71' : pct >= 40 ? '#f39c12' : '#e74c3c';
  const label = pct >= 70 ? 'Clear path to freedom' : pct >= 40 ? 'Partial leverage' : 'Foot-soldier trap';

  return (
    <div className="liberation-meter">
      <div className="liberation-meter-header">
        <div className="liberation-meter-title">Liberation Score</div>
        <div className="liberation-meter-value" style={{ color }}>{pct}%</div>
      </div>
      <div className="liberation-bar-track">
        <div
          className="liberation-bar-fill"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
      <div className="liberation-meter-label" style={{ color }}>{label}</div>
    </div>
  );
}

export default function DecompressionDash({ decompressionData }) {
  if (!decompressionData) return null;

  const { power_map, liberation_score, tensions, strategic_alignment } = decompressionData;

  return (
    <div className="decompression-dash">
      <div className="dash-header">
        <div className="dash-title">Power Analysis Dashboard</div>
        <div className="dash-subtitle">Strategic leverage & liberation analysis</div>
      </div>

      {liberation_score != null && <LiberationMeter score={liberation_score} />}

      <div className="dash-grid">
        <AgentRadarChart powerMap={power_map} />
        <SignalCards powerMap={power_map} />
      </div>

      {tensions && tensions.length > 0 && (
        <div className="tensions-section">
          <div className="tensions-title">Strategic Tensions</div>
          <div className="tensions-list">
            {tensions.map((tension, i) => {
              const agentA = AGENT_META[tension.agent_a];
              const agentB = AGENT_META[tension.agent_b];
              return (
                <div key={i} className="tension-item">
                  <div className="tension-agents">
                    {agentA && (
                      <span className="tension-agent" style={{ color: agentA.color }}>
                        {agentA.icon} {agentA.name}
                      </span>
                    )}
                    <span className="tension-vs">vs</span>
                    {agentB && (
                      <span className="tension-agent" style={{ color: agentB.color }}>
                        {agentB.icon} {agentB.name}
                      </span>
                    )}
                  </div>
                  <p className="tension-description">{tension.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {strategic_alignment && (
        <div className="alignment-section">
          <div className="alignment-title">Strategic Alignment</div>
          <div className="alignment-row">
            {strategic_alignment.aligns_with && strategic_alignment.aligns_with.length > 0 && (
              <div className="alignment-group aligns">
                <span className="alignment-label">Aligns with</span>
                <div className="alignment-agents">
                  {strategic_alignment.aligns_with.map((key) => {
                    const meta = AGENT_META[key];
                    return meta ? (
                      <span key={key} className="alignment-agent" style={{ color: meta.color }}>
                        {meta.icon} {meta.name}
                      </span>
                    ) : null;
                  })}
                </div>
              </div>
            )}
            {strategic_alignment.overrides && strategic_alignment.overrides.length > 0 && (
              <div className="alignment-group overrides">
                <span className="alignment-label">Overrides</span>
                <div className="alignment-agents">
                  {strategic_alignment.overrides.map((key) => {
                    const meta = AGENT_META[key];
                    return meta ? (
                      <span key={key} className="alignment-agent" style={{ color: meta.color }}>
                        {meta.icon} {meta.name}
                      </span>
                    ) : null;
                  })}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
