import AgentRadarChart from './RadarChart';
import SignalCards from './SignalCards';
import './DecompressionDash.css';

const AGENT_META = {
  sentinel: { name: 'Sentinel', icon: '🛡️', color: '#e74c3c' },
  scout: { name: 'Scout', icon: '🔭', color: '#2ecc71' },
  historian: { name: 'Historian', icon: '📚', color: '#3498db' },
  mirror: { name: 'Mirror', icon: '🪞', color: '#9b59b6' },
};

export default function DecompressionDash({ decompressionData }) {
  if (!decompressionData) return null;

  const { compression_map, tensions, recommendation_alignment } = decompressionData;

  return (
    <div className="decompression-dash">
      <div className="dash-header">
        <div className="dash-title">Decision Intelligence Dashboard</div>
        <div className="dash-subtitle">Cognitive compression analysis</div>
      </div>

      <div className="dash-grid">
        <AgentRadarChart compressionMap={compression_map} />
        <SignalCards compressionMap={compression_map} />
      </div>

      {tensions && tensions.length > 0 && (
        <div className="tensions-section">
          <div className="tensions-title">Key Tensions</div>
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

      {recommendation_alignment && (
        <div className="alignment-section">
          <div className="alignment-title">Recommendation Alignment</div>
          <div className="alignment-row">
            {recommendation_alignment.aligns_with &&
              recommendation_alignment.aligns_with.length > 0 && (
                <div className="alignment-group aligns">
                  <span className="alignment-label">Aligns with</span>
                  <div className="alignment-agents">
                    {recommendation_alignment.aligns_with.map((key) => {
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
            {recommendation_alignment.overrides &&
              recommendation_alignment.overrides.length > 0 && (
                <div className="alignment-group overrides">
                  <span className="alignment-label">Overrides</span>
                  <div className="alignment-agents">
                    {recommendation_alignment.overrides.map((key) => {
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
