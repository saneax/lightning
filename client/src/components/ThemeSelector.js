import React, { useState, useEffect } from 'react';
import api from '../services/api';
import '../styles/ThemeSelector.css';

function ThemeSelector({ currentTheme, onThemeSelect, onClose }) {
  const [themes, setThemes] = useState([]);

  useEffect(() => {
    loadThemes();
  }, []);

  const loadThemes = async () => {
    try {
      const response = await api.get('/api/themes');
      setThemes(response.data);
    } catch (error) {
      console.error('Failed to load themes:', error);
    }
  };

  return (
    <div className="theme-selector">
      <div className="theme-selector-header">
        <h3>Select Chat Theme</h3>
        <button onClick={onClose}>&times;</button>
      </div>
      <div className="theme-options">
        {themes.map(theme => (
          <div
            key={theme.id}
            className={`theme-option ${currentTheme?.id === theme.id ? 'selected' : ''}`}
            onClick={() => onThemeSelect(theme.id)}
            style={{
              '--primary': theme.primary_color,
              '--secondary': theme.secondary_color,
              '--text': theme.text_color,
              '--accent': theme.accent_color
            }}
          >
            <div className="theme-preview">
              <div className="preview-message sent">Hello</div>
              <div className="preview-message received">Hi there!</div>
            </div>
            <span className="theme-name">{theme.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ThemeSelector; 