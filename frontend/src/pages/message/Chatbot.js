import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useCurrentUser } from '../../auth/useCurrentUser';
import './Chatbot.css';

const Chatbot = () => {
  const { chatTitle } = useParams(); // chatTitle is used as the groupchat_name
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const { currentUser, setCurrentUser } = useCurrentUser();
  const userId = 1; // Hardcoded user_id for the current user

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

  const handleSend = () => {
    if (input.trim()) {
      const newMessage = { text: input, user_id: userId }; // Include user_id

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
            className={`message ${msg.user_id === userId ? 'user' : 'bot'}`} // Align based on user_id
          >
            {msg.text}
            <br />
          {currentUser.first_name + " " + currentUser.last_name}
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
