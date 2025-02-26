import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import '../styles/ThemeToggle.css';

function ThemeToggle() {
  const { darkMode, toggleTheme } = useTheme();

  return (
    <div className="theme-toggle">
      <label className="switch">
        <input
          type="checkbox"
          checked={darkMode}
          onChange={toggleTheme}
        />
        <span className="slider round"></span>
      </label>
      <span className="theme-label">{darkMode ? 'Dark Mode' : 'Light Mode'}</span>
    </div>
  );
}

export default ThemeToggle; 