import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function PrivateRoute({ component: Component, ...rest }) {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Route
      {...rest}
      render={props => {
        return user ? <Component {...props} /> : <Redirect to="/login" />;
      }}
    />
  );
}

export default PrivateRoute; 