import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useCurrentUser } from '../../auth/useCurrentUser';
import './Chatbot.css';

const Chatbot = () => {
  const { chatTitle } = useParams(); // chatTitle is used as the groupchat_name
  const [messages, setMessages] = useState([]);
  const [userEmails, setUserEmails] = useState({});
  const [input, setInput] = useState('');
  const { currentUser, setCurrentUser } = useCurrentUser();
  // Hardcoded user_id for the current user

  // Fetch messages from the database for the current groupchat on component mount
  useEffect(() => {
    fetch(`/b/messages/${chatTitle}/all_messages`, {
      method: 'GET',
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => setMessages(data))
      .catch((error) => console.error('Error fetching messages:', error));
  }, [chatTitle]);

  // Fetch email for each user_id and cache it
  useEffect(() => {
    const uniqueUserIds = [...new Set(messages.map((msg) => msg.user_id))];
    uniqueUserIds.forEach((id) => {
      if (!userEmails[id]) {
        fetch(`/b/users/${id}`)
          .then((response) => {
            if (!response.ok) {
              throw new Error(`Failed to fetch user email for user_id: ${id}`);
            }
            return response.json();
          })
          .then((user) => {
            setUserEmails((prev) => ({ ...prev, [id]: user.email }));
          })
          .catch((error) =>
            console.error(`Error fetching user email for user_id ${id}:`, error)
          );
      }
    });
  }, [messages, userEmails]);

  const handleSend = () => {
    if (input.trim()) {
      const newMessage = { text: input, user_id: currentUser.id }; // Include user_id

      // Add the new message to the database for the current groupchat
      fetch(`/b/messages/${chatTitle}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newMessage),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((savedMessage) => {
          setMessages([...messages, savedMessage]);
          setInput('');
        })
        .catch((error) => console.error('Error sending message:', error));
    }
  };

  return (
    <div className="chatbot">
      <h1>Chat with {chatTitle}</h1>
      <div className="message-list">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`message ${msg.user_id === currentUser.id ? 'user' : 'bot'}`}
          >
            <strong>
              {userEmails[msg.user_id] || 'Loading email...'}
            </strong>
            <br />
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
