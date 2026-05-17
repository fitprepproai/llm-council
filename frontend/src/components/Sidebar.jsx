import './Sidebar.css';

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
}) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1>Power Council</h1>
        <p className="sidebar-subtitle">48 Laws of Power</p>
        <button className="new-conversation-btn" onClick={onNewConversation}>
          + New Analysis
        </button>
      </div>

      <div className="conversation-list">
        {conversations.length === 0 ? (
          <div className="no-conversations">
            No analyses yet.<br />Start a new conversation to consult the council.
          </div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              className={`conversation-item ${
                conv.id === currentConversationId ? 'active' : ''
              }`}
              onClick={() => onSelectConversation(conv.id)}
            >
              <div className="conversation-title">
                {conv.title || 'New Analysis'}
              </div>
              <div className="conversation-meta">
                {conv.message_count} {conv.message_count === 1 ? 'message' : 'messages'}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
