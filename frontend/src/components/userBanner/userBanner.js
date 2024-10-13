import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './userBanner.css';
import { CurrentUser } from '../../App'

const UserBanner = (props) => {
  const { currentUser, setCurrentUser } = useContext(CurrentUser);
  const navigate = useNavigate();

  const handleSignOut = () => {
    setCurrentUser(null);
    navigate("/login");
  };

  return (
    <div className="user-banner-container">
      <span>Welcome, { currentUser.first_name } { currentUser.last_name }!</span>
      <button className="btn sign-out-btn" onClick={handleSignOut}>Sign out</button>
    </div>
  );
}

export default UserBanner;
