import React, { useState } from 'react';
import './ChatInput.css';

export const ChatInput = ({ onSendMessage, disabled }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-input-wrapper">
      <div className="chat-input-container">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask anything about Sierra AI..."
          disabled={disabled}
          rows={1}
          className="chat-input-textarea"
          style={{ minHeight: '56px', maxHeight: '200px' }}
          onInput={(e) => {
            e.target.style.height = 'auto';
            e.target.style.height = e.target.scrollHeight + 'px';
          }}
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || disabled}
          className="chat-input-button"
        >
          Send
        </button>
      </div>
    </div>
  );
};
