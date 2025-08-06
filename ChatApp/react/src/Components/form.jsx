import React, { useState, useEffect, useRef, useLayoutEffect } from 'react'
import { ChatHeader } from './ChatHeader'
import { MessageInput } from './MessageInput'
import { MessageList } from './MessageList'
import { ConnectionInfo } from './ConnectionInfo'
import './ChatContainer.css'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/all'
gsap.registerPlugin(ScrollTrigger)



export const Form = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    // Use environment variable or fallback to localhost
    const wsUrl = import.meta.env.VITE_WEBSOCKET_URL || "ws://localhost:8000/ws";
    console.log("Connecting to WebSocket:", wsUrl);
    
    const ws = new WebSocket(wsUrl); 
    wsRef.current = ws;                                 

    ws.onopen = () => {                                 
      console.log("WebSocket connection established");  
      setIsConnected(true);                             
    };

    ws.onmessage = (event) => {                         
      const messageData = JSON.parse(event.data);       
      console.log("Message from server:", messageData); 
      setMessages(prev => [...prev, messageData]);       
    };                                                  

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setIsConnected(false);
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
      setIsConnected(false);
    };

    // Cleanup WebSocket connection on component unmount
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, []);

  const handleMessageSubmit = (messageContent) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      // Add the message locally for the sender
      const localMessage = {
        type: "message",
        client: "You",
        content: messageContent,
        timestamp: new Date().toISOString(),
        isOwnMessage: true
      };
      
      // Add to local messages immediately
      setMessages(prev => [...prev, localMessage]);
      
      // Send to server (will broadcast to other clients only)
      wsRef.current.send(JSON.stringify({ type: "message", content: messageContent }));
    }
  };

  const boxRef = useRef(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      // Set initial state
      gsap.set(boxRef.current, { opacity: 0, x: -50 });
      
      // Create timeline with ScrollTrigger
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: boxRef.current,
          start: "top 80%",
          end: "bottom 20%",
          toggleActions: "restart reverse play reverse"
        }
      });
      
      tl.to(boxRef.current, {
        opacity: 1,
        x: 0,
        duration: 1,
        ease: "power2.out"
      });
    }, boxRef);
    
    return () => ctx.revert();
  }, []); // Fixed dependency array 

  return (
    <div className="chat-container">
      <ChatHeader isConnected={isConnected} />
      <div ref={boxRef}>
        <MessageInput 
          message={message}
          setMessage={setMessage}
          onSubmit={handleMessageSubmit}
          isConnected={isConnected}
        />
      </div>
      <MessageList messages={messages} />
      <ConnectionInfo wsUrl={import.meta.env.VITE_WEBSOCKET_URL} />
    </div>
  )
}
