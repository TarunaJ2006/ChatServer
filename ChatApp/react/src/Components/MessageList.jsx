import React from 'react';
import { MessageBubble } from './MessageBubble';
import './MessageList.css';

export const MessageList = ({ messages }) => {
  return (
    <div className="messages-container">
      <div className="messages-header">
        Messages ({messages.length})
      </div>
      <div className="messages-list">
        {messages.length === 0 ? (
          <p className="no-messages">No messages yet</p>
        ) : (
          messages.map((msg, index) => (
            <MessageBubble key={index} message={msg} index={index} />
          ))
        )}
      </div>
    </div>
  );
};
