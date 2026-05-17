import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './Stage2.css';

function deAnonymizeText(text, labelToAgent) {
  if (!labelToAgent) return text;
  let result = text;
  Object.entries(labelToAgent).forEach(([label, agentInfo]) => {
    const display = `**${agentInfo.icon} ${agentInfo.name}**`;
    result = result.replace(new RegExp(label, 'g'), display);
  });
  return result;
}

export default function Stage2({ rankings, labelToAgent, aggregateRankings }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!rankings || rankings.length === 0) {
    return null;
  }

  const active = rankings[activeTab];

  return (
    <div className="stage stage2">
      <h3 className="stage-title">Stage 2 — Cross-Examination</h3>
      <p className="stage-description">
        Each cognitive agent evaluates the others' analyses through its bias lens — anonymized during evaluation.
        Agent names shown in <strong>bold</strong> are for readability only.
      </p>

      <div className="tabs">
        {rankings.map((rank, index) => (
          <button
            key={index}
            className={`tab ${activeTab === index ? 'active' : ''}`}
            style={activeTab === index ? { borderColor: rank.color, color: rank.color } : {}}
            onClick={() => setActiveTab(index)}
          >
            {rank.icon} {rank.name}
          </button>
        ))}
      </div>

      <div className="tab-content" style={{ borderTopColor: active.color }}>
        <div className="agent-header" style={{ borderLeftColor: active.color }}>
          <div>
            <div className="agent-name" style={{ color: active.color }}>
              {active.icon} {active.name}
            </div>
            <div className="agent-description">Cross-Examiner</div>
          </div>
        </div>

        <div className="ranking-content markdown-content">
          <ReactMarkdown>
            {deAnonymizeText(active.ranking, labelToAgent)}
          </ReactMarkdown>
        </div>

        {active.parsed_ranking && active.parsed_ranking.length > 0 && (
          <div className="parsed-ranking">
            <strong>Extracted Ranking</strong>
            <ol>
              {active.parsed_ranking.map((label, i) => {
                const agentInfo = labelToAgent && labelToAgent[label];
                return (
                  <li key={i}>
                    {agentInfo ? `${agentInfo.icon} ${agentInfo.name}` : label}
                  </li>
                );
              })}
            </ol>
          </div>
        )}
      </div>

      {aggregateRankings && aggregateRankings.length > 0 && (
        <div className="aggregate-rankings">
          <h4>Aggregate Rankings</h4>
          <p className="aggregate-description">
            Combined scores across all peer cross-examinations (lower = ranked more useful by peers):
          </p>
          <div className="aggregate-list">
            {aggregateRankings.map((agg, index) => (
              <div key={index} className="aggregate-item">
                <span className="rank-position" style={{ color: agg.color }}>#{index + 1}</span>
                <span className="rank-icon">{agg.icon}</span>
                <span className="rank-model">{agg.name}</span>
                <span className="rank-score">avg {agg.average_rank.toFixed(2)}</span>
                <span className="rank-count">({agg.rankings_count} votes)</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
