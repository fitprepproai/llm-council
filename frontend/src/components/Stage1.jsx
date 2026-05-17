import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './Stage1.css';

export default function Stage1({ responses }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!responses || responses.length === 0) {
    return null;
  }

  const active = responses[activeTab];

  return (
    <div className="stage stage1">
      <h3 className="stage-title">Stage 1 — Cognitive Analysis</h3>
      <p className="stage-description">
        Each agent analyzes the situation through its specialized cognitive lens.
      </p>

      <div className="tabs">
        {responses.map((resp, index) => (
          <button
            key={index}
            className={`tab ${activeTab === index ? 'active' : ''}`}
            style={activeTab === index ? { borderColor: resp.color, color: resp.color } : {}}
            onClick={() => setActiveTab(index)}
          >
            {resp.icon} {resp.name}
          </button>
        ))}
      </div>

      <div className="tab-content" style={{ borderTopColor: active.color }}>
        <div className="agent-header" style={{ borderLeftColor: active.color }}>
          <div>
            <div className="agent-name" style={{ color: active.color }}>
              {active.icon} {active.name}
            </div>
            <div className="agent-description">{active.description}</div>
          </div>
        </div>
        <div className="response-text markdown-content">
          <ReactMarkdown>{active.response}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
