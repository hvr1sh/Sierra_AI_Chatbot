import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { sendChatMessage } from '../services/api';
import sierraLogo from '../assets/sierra-logo.svg';
import './ChatContainer.css';

export const ChatContainer = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content) => {
    const userMessage = {
      role: 'user',
      content,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendChatMessage(content);
      console.log(response)
      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);

      const errorAssistantMessage = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}`,
      };

      setMessages((prev) => [...prev, errorAssistantMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="chat-header-content">
          <div className="chat-header-title-wrapper">
            <div className="chat-header-icon">
              <img src={sierraLogo} alt="Sierra AI" />
            </div>
            <div>
              <h1 className="chat-header-title">Sierra AI Assistant</h1>
              <p className="chat-header-subtitle">
                Powered by conversational AI
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages-wrapper">
        <div className="chat-messages-content">
          {messages.length === 0 && (
            <div className="chat-welcome">
              <div className="chat-welcome-icon">
                <img src={sierraLogo} alt="Sierra AI" />
              </div>
              <h2 className="chat-welcome-title">
                Welcome to Sierra AI
              </h2>
              <p className="chat-welcome-description">
                Ask me anything about Sierra, our conversational AI platform, values, and opportunities
              </p>
              <div className="chat-suggestions">
                {[
                  "What is Sierra AI?",
                  "Who founded Sierra?",
                  "What does Sierra's product do?",
                  "Tell me about Sierra's mission",
                ].map((suggestion, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(suggestion)}
                    className="chat-suggestion-button"
                  >
                    <span>{suggestion}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((message, idx) => (
            <ChatMessage key={idx} message={message} />
          ))}

          {isLoading && (
            <div className="chat-loading">
              <div className="chat-loading-bubble">
                <div className="chat-loading-dots">
                  <div className="chat-loading-dot"></div>
                  <div className="chat-loading-dot"></div>
                  <div className="chat-loading-dot"></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  );
};
