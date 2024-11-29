import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './Chatbot.css';

const Chatbot = () => {
  const { chatTitle } = useParams();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  // Base URL for the backend


  // Fetch messages from the database on component mount
  useEffect(() => {
    fetch(`/b/messages`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => setMessages(data))
      .catch((error) => console.error('Error fetching messages:', error));
  }, []);

  const handleSend = () => {
    if (input.trim()) {
      const newMessage = { text: input, is_user: true };

      // Add the new message to the database
      fetch(`b/messages/`, {
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

          // Simulate a bot response
          setTimeout(() => {
            const botMessage = { text: 'Got it! How can I help you?', is_user: false };

            fetch(`b/messages/`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(botMessage),
            })
              .then((response) => {
                if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
              })
              .then((savedBotMessage) => {
                setMessages((prevMessages) => [...prevMessages, savedBotMessage]);
              })
              .catch((error) => console.error('Error sending bot message:', error));
          }, 1000);
        })
        .catch((error) => console.error('Error sending message:', error));
    }
  };

  return (
    <div className='chatbot'>
      <h1>Chat with {chatTitle}</h1>
      <div className='message-list'>
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.is_user ? 'user' : 'bot'}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className='input-area'>
        <input
          type='text'
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder='Type your message...'
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
