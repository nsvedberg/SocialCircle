import React from 'react';
import { Link } from 'react-router-dom';
import './nav.css'; 



const nav = () => {


    return (
        <nav className="bottom-nav">
          <Link to="/dashboard" className="nav-item">
            <span role="img" aria-label="home">🏠</span>
            <p>Dashboard</p>
          </Link>
          <Link to="/messages" className="nav-item">
          <span role="img" aria-label="message">💬</span>
            <p>Messages</p>
          </Link>
          <Link to="/profile" className="nav-item">
            <span role="img" aria-label="profile">👤</span>
            <p>Profile</p>
          </Link>
        </nav>
      );
}

export default nav;