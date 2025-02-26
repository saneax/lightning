import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import io from 'socket.io-client';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

function Channel() {
  const { channelId } = useParams();
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const socketRef = useRef();

  useEffect(() => {
    // Connect to WebSocket
    socketRef.current = io(process.env.REACT_APP_API_URL, {
      query: { channelId },
      withCredentials: true
    });

    // Load existing messages
    api.get(`/api/channels/${channelId}/messages`)
      .then(response => {
        setMessages(response.data);
      });

    // Listen for new messages
    socketRef.current.on('message', message => {
      setMessages(prev => [...prev, message]);
    });

    return () => {
      socketRef.current.disconnect();
    };
  }, [channelId]);

  const sendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim()) {
      socketRef.current.emit('message', {
        channelId,
        content: newMessage
      });
      setNewMessage('');
    }
  };

  return (
    <div className="channel">
      <div className="messages">
        {messages.map(message => (
          <div key={message.id} className="message">
            <strong>{message.username}</strong>
            <p>{message.content}</p>
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage}>
        <input
          type="text"
          value={newMessage}
          onChange={e => setNewMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default Channel; 