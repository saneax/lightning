import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import ThemeToggle from './ThemeToggle';
import api from '../services/api';
import '../styles/Dashboard.css';

function Dashboard() {
  const [channels, setChannels] = useState([]);
  const [newChannel, setNewChannel] = useState({ name: '', description: '', isPrivate: false });
  const { user } = useAuth();

  useEffect(() => {
    loadChannels();
  }, []);

  const loadChannels = async () => {
    try {
      const response = await api.get('/api/channels');
      setChannels(response.data);
    } catch (error) {
      console.error('Failed to load channels:', error);
    }
  };

  const handleCreateChannel = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/api/channels', newChannel);
      setChannels([...channels, response.data]);
      setNewChannel({ name: '', description: '', isPrivate: false });
    } catch (error) {
      console.error('Failed to create channel:', error);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome, {user.username}!</h1>
        <ThemeToggle />
      </div>
      
      <div className="channels-section">
        <h2>Your Channels</h2>
        <div className="channels-list">
          {channels.map(channel => (
            <Link 
              key={channel.id} 
              to={`/channel/${channel.id}`}
              className="channel-card"
            >
              <h3>{channel.name}</h3>
              <p>{channel.description}</p>
              {channel.isPrivate && <span className="private-badge">Private</span>}
            </Link>
          ))}
        </div>
      </div>

      <div className="create-channel">
        <h2>Create New Channel</h2>
        <form onSubmit={handleCreateChannel}>
          <div className="form-group">
            <input
              type="text"
              placeholder="Channel Name"
              value={newChannel.name}
              onChange={(e) => setNewChannel({...newChannel, name: e.target.value})}
              required
            />
          </div>
          <div className="form-group">
            <textarea
              placeholder="Channel Description"
              value={newChannel.description}
              onChange={(e) => setNewChannel({...newChannel, description: e.target.value})}
            />
          </div>
          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={newChannel.isPrivate}
                onChange={(e) => setNewChannel({...newChannel, isPrivate: e.target.checked})}
              />
              Private Channel
            </label>
          </div>
          <button type="submit">Create Channel</button>
        </form>
      </div>
    </div>
  );
}

export default Dashboard; 