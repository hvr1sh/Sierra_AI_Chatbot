import React from 'react';
import './ChatMessage.css';

export const ChatMessage = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`message-wrapper ${isUser ? 'user' : 'assistant'}`}>
      <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
        <div className="message-content">{message.content}</div>

        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            <div className="message-sources-label">Sources:</div>
            <div className="message-sources-list">
              {message.sources.map((source, idx) => (
                <a
                  key={idx}
                  href={source}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="message-source-link"
                >
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  {new URL(source).pathname || 'Link'}
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
