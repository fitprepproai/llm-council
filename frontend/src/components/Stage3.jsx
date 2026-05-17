import ReactMarkdown from 'react-markdown';
import DecompressionDash from './DecompressionDash';
import './Stage3.css';

export default function Stage3({ finalResponse }) {
  if (!finalResponse) {
    return null;
  }

  return (
    <div className="stage stage3">
      <h3 className="stage-title">Stage 3 — Decompression Report</h3>

      {finalResponse.decompression_data && (
        <DecompressionDash decompressionData={finalResponse.decompression_data} />
      )}

      <div className="final-response">
        <div className="chairman-label">
          Decompressor
        </div>
        <div className="final-text markdown-content">
          <ReactMarkdown>{finalResponse.response}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
