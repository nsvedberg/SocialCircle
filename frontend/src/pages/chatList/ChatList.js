import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './ChatList.css';
import Nav from '../../components/nav/nav';
import { useCurrentUser } from '../../auth/useCurrentUser';

const ChatList = () => {
  const { user } = useCurrentUser(); // Get the current user's details
  const [chats, setChats] = useState([]); // State to hold the user's clubs
  const { currentUser, setCurrentUser } = useCurrentUser();

  useEffect(() => {
    // Fetch the user's clubs from the backend
    const fetchClubs = async () => {
      try {
        const response = await fetch(`/b/users/${currentUser.id}/clubs`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const clubsData = await response.json();
          console.log(clubsData)
          // Map the clubs to match the structure of chat items
          const chatItems = clubsData.map(club => ({
            id: club.id,
            name: club.club_name,
            lastMessage: `Welcome to ${club.club_name}!`, // Placeholder last message
          }));
          
          setChats(chatItems);
        } else {
          console.error('Failed to fetch clubs');
        }
      } catch (error) {
        console.error('Error fetching clubs:', error);
      }
    };

    if (currentUser?.id) {
      fetchClubs();
    }
  }, [currentUser]);

  return (
    <div className='chat-list'>
      <Nav />
      <h1>Messages</h1>
      <ul>
        {chats.map(chat => (
          <li key={chat.name} className='chat-item'>
            <Link to={`/chat/${chat.name}`} className='chat-link'>
              <div className='chat-info'>
                <h2>{chat.name}</h2>
                <p>{chat.lastMessage}</p>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChatList;
