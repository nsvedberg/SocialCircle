import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import './Chatbot.css';

const Chatbot = () => {
  const { chatId } = useParams(); // Get chatId from URL
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, isUser: true }]);
      setInput('');

      // Simulate a response from chatbot
      setTimeout(() => {
        setMessages([...messages, { text: input, isUser: true }, { text: 'Got it! How can I help you?', isUser: false }]);
      }, 1000);
    }
  };

  return (
    <div className='chatbot'>
      <h1>Chat with {chatId}</h1>
      <div className='message-list'>
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.isUser ? 'user' : 'bot'}`}>
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
