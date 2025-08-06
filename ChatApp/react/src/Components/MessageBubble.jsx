import React from 'react';
import './MessageBubble.css';
import gsap from 'gsap';
import { SplitText } from 'gsap/all';

gsap.registerPlugin(SplitText);


export const MessageBubble = ({ message, index }) => {
  const getMessageClass = () => {
    if (message.isOwnMessage) return 'own-message';
    if (message.type === 'system') return 'system-message';
    if (message.type === 'notification') return 'notification-message';
    return 'regular-message';
  };
  const boxRef = React.useRef(null);

  React.useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      const split = new SplitText(boxRef.current, { type: "chars" });

      gsap.fromTo(split.chars, {
        y: (index) => index % 2 === 0 ? -3 : 3,
        opacity: 0,
      }, {
        y: 0,
        opacity: 1,
        duration: 0.1,
        ease: "power2.out",
        stagger: 0.1
      });
    }, boxRef);
    return () => ctx.revert();
  }, []);

  return (
    <div className={`message-item ${getMessageClass()}`}>
      <div className="message-header">
        {message.timestamp && new Date(message.timestamp).toLocaleTimeString()}
        {message.client && ` - ${message.client}`}
      </div>
      <div ref={boxRef} className="message-content">
        {message.content || message.message}
      </div>
      
      
    </div>
  );
};
