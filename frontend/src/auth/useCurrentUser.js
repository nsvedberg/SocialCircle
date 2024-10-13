import { useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';

export function useCurrentUser() {
  const getCurrentUser = () => {
    const str = sessionStorage.getItem('currentUser');
    return JSON.parse(str);
  };

  const [currentUser, setCurrentUser] = useState(getCurrentUser());

  const saveCurrentUser = newUser => {
    sessionStorage.setItem('currentUser', JSON.stringify(newUser));
    setCurrentUser(newUser);
  };

  return {
    currentUser,
    setCurrentUser: saveCurrentUser
  }
}

export function RequireAuth({ children }) {
  let { currentUser, setCurrentUser } = useCurrentUser();
  let location = useLocation();

  console.log(currentUser);

  if (!currentUser) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
