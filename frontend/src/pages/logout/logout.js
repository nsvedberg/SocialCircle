import { useContext, useEffect } from "react";
import { CurrentUser } from '../../App';
import { Navigate } from 'react-router-dom';

const Logout = () => {
  const { currentUser, setCurrentUser } = useContext(CurrentUser);

  useEffect(() => {
    setCurrentUser(null);
  });

  return <Navigate to="/login" replace />;
};

export default Logout;
