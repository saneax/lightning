import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import PrivateRoute from './components/PrivateRoute';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import Channel from './components/Channel';
import DirectMessage from './components/DirectMessage';
import './styles/App.css';

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <Router>
          <Switch>
            <Route exact path="/login" component={Login} />
            <Route exact path="/register" component={Register} />
            <PrivateRoute exact path="/" component={Dashboard} />
            <PrivateRoute exact path="/channel/:channelId" component={Channel} />
            <PrivateRoute exact path="/messages/:userId" component={DirectMessage} />
          </Switch>
        </Router>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App; 