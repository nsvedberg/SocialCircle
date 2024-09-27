import React from 'react';
import { Link } from 'react-router-dom';
import './ChatList.css';

const ChatList = () => {
  // Example chats data
  const chats = [
    { id: 1, name: 'John Doe', lastMessage: 'Hey, how are you?' },
    { id: 2, name: 'Jane Smith', lastMessage: 'Can we meet tomorrow?' },
    { id: 3, name: 'Michael Brown', lastMessage: 'I finished the project!' },
    // Add more chats as needed
  ];

  return (
    <div className='chat-list'>
      <h1>Messages</h1>
      <ul>
        {chats.map(chat => (
          <li key={chat.id} className='chat-item'>
            <Link to={`/chat/${chat.id}`} className='chat-link'>
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
