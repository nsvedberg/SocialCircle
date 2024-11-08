import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './user.css';
import Nav from '../../components/nav/nav';
import { useCurrentUser } from '../../auth/useCurrentUser';

const User = () => {
  let { currentUser, setCurrentUser } = useCurrentUser();
  let [user, setUser] = useState({});

  const { id } = useParams();

  const fetchUser = async () => {
    const response = await fetch("/b/users/" + id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const json = await response.json();

    return json;
  }

  useEffect(() => {
    fetchUser().then((user) => { setUser(user) });
  }, []);

  return (
    <div className='user-container'>
      <div className='user-profile'>
        <h1>{user.first_name} {user.last_name}</h1>
        <div className='user-sect user-grad-year'>
          <span className='user-sect-label'>Grad Year: </span>
          {user.grad_year}
        </div>
        <div className='user-sect user-interests'>
          <span className='user-sect-label'>Interests: </span>
          {user.interests}
        </div>
        <div className='user-sect user-bio'>
          <span className='user-sect-label'>Bio: </span>
          {user.bio}
        </div>
      </div>
      <Nav />
    </div>
  );
};

export default User;
