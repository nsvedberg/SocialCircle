import React from 'react';
import { useNavigate } from 'react-router-dom';
import './create.css';

const CreateEventButton = () => {
  let navigate = useNavigate();

  const sendToCreateEvent = () => {
    navigate('/b/events/new'); // This takes us to the event creation page
  };

  return (
    <div className="create-button-container">
      <h1>Events</h1>
      <button className="create-button" onClick={sendToCreateEvent}>+</button>
    </div>
  );
};

export default CreateEventButton;
