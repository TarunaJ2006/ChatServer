import React from 'react';
import './ConnectionInfo.css';


export const ConnectionInfo = ({ wsUrl }) => {
  return (
    <div className="connection-info">
        WebSocket: {wsUrl}
    </div>
  );
};
