import { useState } from 'react';
import Nav from '../../components/nav/nav';
import './createEvent.css';
import { useNavigate } from "react-router-dom";

import { useCurrentUser } from '../../auth/useCurrentUser';

const CreateEvent = () => {
  const { currentUser, setCurrentUser } = useCurrentUser();

  const [formValues, setFormValues] = useState({
    "name": "",
    "description": "",
  });
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormValues({ ...formValues, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log(formValues);

    const token = currentUser.token;

    const response = await fetch("/b/events/new", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify(formValues),
    });

    const body = response.json();

    if (response.ok) {
      alert("Created event successfully!");
    } else {
      console.log("Error creating event", body.error);
      console.log(body.message);

      return null;
    }
  }

  return (
    <div>
      <h1>Create a new event!</h1>
      <Nav />
      <form onSubmit={handleSubmit} className="create-event-form">
        <div className="form-group">
          <label htmlFor="event-name">Event Name</label>
          <input
            type="text"
            id="event-name"
            name="name"
            value={formValues.name}
            onChange={handleInputChange}
            className="form-input"
          />
        </div>
        <div className="form-group">
          <label htmlFor="event-description">Event Description</label>
          <input
            type="text"
            id="event-description"
            name="description"
            value={formValues.description}
            onChange={handleInputChange}
            className="form-input"
          />
        </div>
        <div className="form-group">
          <label htmlFor="event-date">Event Date</label>
          <input
            type="date"
            id="event-date"
            name="date"
            value={formValues.date}
            onChange={handleInputChange}
            className="form-input"
          />
        </div>
        <div className="form-group">
          <label htmlFor="event-time">Event Time</label>
          <input
            type="time"
            id="event-time"
            name="time"
            value={formValues.time}
            onChange={handleInputChange}
            className="form-input"
          />
        </div>
        <div className="form-group">
          <label htmlFor="event-location">Event Location</label>
          <input
            type="text"
            id="event-location"
            name="location"
            value={formValues.location}
            onChange={handleInputChange}
            className="form-input"
          />
        </div>
        <div className="form-group">
          <label htmlFor="event-club">Event Club</label>
          <input
            type="text"
            id="event-club"
            name="club"
            value={formValues.club}
            onChange={handleInputChange}
            className="form-input"
          />
        </div>
        <button type="submit" className="create-event-button">Create Event</button>
      </form>
    </div>
  );
};

export default CreateEvent;
