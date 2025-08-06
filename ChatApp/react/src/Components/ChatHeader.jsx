import React, { useLayoutEffect, useRef } from 'react';
import './ChatHeader.css';
import gsap from 'gsap';
import { SplitText } from 'gsap/all';
import { ScrollTrigger } from 'gsap/all';
gsap.registerPlugin(ScrollTrigger);

gsap.registerPlugin(SplitText);

export const ChatHeader = ({ isConnected, title = "Group Chat" }) => {
  const boxRef = useRef(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      const split = new SplitText(boxRef.current, { type: "chars" });
      
      gsap.fromTo(split.chars, {

        opacity: 0,
      }, {
        y: 0,
        opacity: 1,
        duration: 0.05,
        ease: "bounce.out",
        stagger: {
            from : "center",
            amount: 0.5,
            grid: "auto",
            each: 0.05
        }
      });
    }, boxRef);
    return () => ctx.revert();
  }, []); // Added dependency array

  return (
    <div className="chat-header">
      <h1 className="chat-title">{title}</h1>
      <div ref={boxRef}>
        Fully anonymous if you use a VPN
      </div>
      <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
        {isConnected ? '✅ Connected' : '❌ Disconnected'}
      </div>
    </div>
  );
};
