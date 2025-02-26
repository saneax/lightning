import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';
import ThemeSelector from './ThemeSelector';
import api from '../services/api';
import '../styles/DirectMessage.css';

function DirectMessage() {
  const { userId } = useParams();
  const { darkMode } = useTheme();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [chatUser, setChatUser] = useState(null);
  const [currentTheme, setCurrentTheme] = useState(null);
  const [showThemeSelector, setShowThemeSelector] = useState(false);

  useEffect(() => {
    loadMessages();
    loadChatUser();
    loadThemePreference();
  }, [userId]);

  const loadMessages = async () => {
    try {
      const response = await api.get(`/api/messages/direct/${userId}`);
      setMessages(response.data);
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };

  const loadChatUser = async () => {
    try {
      const response = await api.get(`/api/users/${userId}`);
      setChatUser(response.data);
    } catch (error) {
      console.error('Failed to load user:', error);
    }
  };

  const loadThemePreference = async () => {
    try {
      const response = await api.get(`/api/preferences/chat/${userId}`);
      setCurrentTheme(response.data.theme);
    } catch (error) {
      console.error('Failed to load theme preference:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    try {
      const response = await api.post(`/api/messages/direct/${userId}`, {
        content: newMessage
      });
      setMessages([...messages, response.data]);
      setNewMessage('');
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleThemeChange = async (themeId) => {
    try {
      await api.post(`/api/preferences/chat/${userId}`, { themeId });
      loadThemePreference();
      setShowThemeSelector(false);
    } catch (error) {
      console.error('Failed to update theme:', error);
    }
  };

  return (
    <div className={`direct-message ${currentTheme?.name.toLowerCase().replace(' ', '-')}`}>
      <div className="dm-header">
        <h2>{chatUser?.username}</h2>
        <button 
          className="theme-button"
          onClick={() => setShowThemeSelector(!showThemeSelector)}
        >
          Change Theme
        </button>
      </div>

      {showThemeSelector && (
        <ThemeSelector
          currentTheme={currentTheme}
          onThemeSelect={handleThemeChange}
          onClose={() => setShowThemeSelector(false)}
        />
      )}

      <div className="messages">
        {messages.map(message => (
          <div 
            key={message.id} 
            className={`message ${message.sender_id === userId ? 'received' : 'sent'}`}
          >
            <p>{message.content}</p>
            <span className="message-time">
              {new Date(message.created_at).toLocaleTimeString()}
            </span>
          </div>
        ))}
      </div>

      <form onSubmit={handleSendMessage} className="message-form">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
          className="message-input"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default DirectMessage; 