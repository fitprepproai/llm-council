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

const AGENT_META = {
  leverage: { label: '⚡ Leverage', color: '#f39c12' },
  position: { label: '♟️ Power', color: '#e74c3c' },
  architect: { label: '🏗️ Long Game', color: '#3498db' },
  freedom: { label: '🔓 Freedom', color: '#2ecc71' },
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

export default function AgentRadarChart({ powerMap }) {
  if (!powerMap) return null;

  const data = Object.entries(AGENT_META).map(([key, meta]) => ({
    axis: meta.label,
    value: Math.round((powerMap[key]?.weight ?? 0) * 100),
    fill: meta.color,
  }));

  return (
    <div className="radar-container">
      <div className="radar-title">Power Analysis</div>
      <div className="radar-subtitle">Signal intensity per strategic lens</div>
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
