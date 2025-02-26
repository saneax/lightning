-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Channels table
CREATE TABLE channels (
    channel_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_private BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(user_id),
    sticky_note TEXT
);

-- Channel members table
CREATE TABLE channel_members (
    channel_id INTEGER REFERENCES channels(channel_id),
    user_id INTEGER REFERENCES users(user_id),
    role VARCHAR(20) NOT NULL CHECK (role IN ('member', 'admin', 'creator')),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (channel_id, user_id)
);

-- Messages table
CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    channel_id INTEGER REFERENCES channels(channel_id),
    user_id INTEGER REFERENCES users(user_id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT false
);

-- Banned users table
CREATE TABLE banned_users (
    channel_id INTEGER REFERENCES channels(channel_id),
    user_id INTEGER REFERENCES users(user_id),
    banned_by INTEGER REFERENCES users(user_id),
    banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason TEXT,
    PRIMARY KEY (channel_id, user_id)
);

-- Direct Messages table
CREATE TABLE direct_messages (
    message_id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users(user_id),
    receiver_id INTEGER REFERENCES users(user_id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT false
);

-- Chat Themes table
CREATE TABLE chat_themes (
    theme_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    primary_color VARCHAR(7) NOT NULL,
    secondary_color VARCHAR(7) NOT NULL,
    text_color VARCHAR(7) NOT NULL,
    accent_color VARCHAR(7) NOT NULL
);

-- User Chat Preferences table
CREATE TABLE user_chat_preferences (
    user_id INTEGER REFERENCES users(user_id),
    chat_with_user_id INTEGER REFERENCES users(user_id),
    theme_id INTEGER REFERENCES chat_themes(theme_id),
    PRIMARY KEY (user_id, chat_with_user_id)
);

-- Insert default themes
INSERT INTO chat_themes (name, primary_color, secondary_color, text_color, accent_color) VALUES
('Default Blue', '#E3F2FD', '#BBDEFB', '#1565C0', '#2196F3'),
('Mint Green', '#E8F5E9', '#C8E6C9', '#2E7D32', '#4CAF50'),
('Warm Purple', '#F3E5F5', '#E1BEE7', '#7B1FA2', '#9C27B0'),
('Sunset Orange', '#FBE9E7', '#FFCCBC', '#D84315', '#FF5722'),
('Dark Mode', '#1A1A1A', '#2D2D2D', '#FFFFFF', '#BB86FC');

-- Create indexes for better performance
CREATE INDEX idx_messages_channel_id ON messages(channel_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_channel_members_user_id ON channel_members(user_id); 