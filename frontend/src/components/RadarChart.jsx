import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import './RadarChart.css';

const QUALITY_COLORS = { HIGH: '#2ecc71', MEDIUM: '#f39c12', LOW: '#e74c3c' };

const AGENT_META = {
  sentinel: { label: '🛡️ Threat', color: '#e74c3c' },
  scout: { label: '🔭 Opportunity', color: '#2ecc71' },
  historian: { label: '📚 Pattern', color: '#3498db' },
  mirror: { label: '🪞 Familiarity', color: '#9b59b6' },
};

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload || !payload.length) return null;
  const item = payload[0];
  return (
    <div className="radar-tooltip">
      <div className="radar-tooltip-label">{item.payload.axis}</div>
      <div className="radar-tooltip-value">{item.value}%</div>
    </div>
  );
};

export default function AgentRadarChart({ compressionMap }) {
  if (!compressionMap) return null;

  const data = Object.entries(AGENT_META).map(([key, meta]) => ({
    axis: meta.label,
    value: Math.round((compressionMap[key]?.weight ?? 0) * 100),
    fill: meta.color,
  }));

  return (
    <div className="radar-container">
      <div className="radar-title">Compression Intensity</div>
      <div className="radar-subtitle">How strongly each cognitive signal fired</div>
      <ResponsiveContainer width="100%" height={280}>
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid stroke="rgba(255,255,255,0.08)" />
          <PolarAngleAxis
            dataKey="axis"
            tick={{ fill: '#9090b0', fontSize: 12 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fill: '#606080', fontSize: 10 }}
            tickCount={4}
          />
          <Radar
            name="Signal"
            dataKey="value"
            stroke="#4a90e2"
            fill="#4a90e2"
            fillOpacity={0.2}
            strokeWidth={2}
          />
          <Tooltip content={<CustomTooltip />} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
