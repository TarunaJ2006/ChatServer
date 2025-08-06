import React from 'react';
import './MessageInput.css';

export const MessageInput = ({ message, setMessage, onSubmit, isConnected }) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    if (message.trim() && isConnected) {
      onSubmit(message);
      setMessage('');
    }
  };

  return (
    <div className="message-form-container">
      <form onSubmit={handleSubmit} className="message-form">
        <input 
          type="text" 
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          className="message-input"
        />
        <button type="submit" disabled={!isConnected} className="send-button">
          Send
        </button>
      </form>
    </div>
  );
};
