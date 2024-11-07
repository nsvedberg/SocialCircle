import { useState, useEffect, useContext } from 'react';
import Nav from '../../components/nav/nav';
import './dashboard.css';
import { CurrentUser } from '../../App';
import { useNavigate } from "react-router-dom";
import CreateEventButton from '../../components/create/CreateEventButton'; // Import CreateEventButton
import UserBanner from '../../components/userBanner/userBanner';

const Dashboard = () => {
  const { currentUser, setCurrentUser } = useContext(CurrentUser);
  const [events, setEvents] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearch = async () => {
    try {
      const data = await fetch(`/b/events?search=${searchTerm}`);
      const eventData = await data.json();
      setEvents(eventData);
    } catch (error) {
      console.error('Error searching for events:', error);
    }
  };

  const clearBar = async () => {
    setSearchTerm("");
    getEvents();
  };

  const getEvents = async () => {
    try {
      const data = await fetch("/b/events");
      const eventData = await data.json();
      setEvents(eventData);
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  useEffect(() => {
    getEvents();
  }, []);

  return (
    <div className='body'>
      <UserBanner />

      <div className="search-container">
        <input
          type="text"
          value={searchTerm}
          onChange={handleInputChange}
          placeholder="Search events..."
          className="search-bar"
        />
        <button onClick={handleSearch} className="search-button">
          Search
        </button>

        <button onClick={clearBar} className="clear-button">
          Clear
        </button>
      </div>

      <CreateEventButton /> {/* This button is only visible on the dashboard */}
      
      <Nav />
      
      <div className="events-container">
        {events.length > 0 ? (
          events.map((event, index) => (
            <div key={index} className="event-card">
              <h2>{event.event_name}</h2>
              <p>{event.event_description}</p>
              <p>Location: {event.event_location}</p>
              <a href={`/event/${event.id}`} rel="noopener noreferrer">View Event</a>
            </div>
          ))
        ) : (
          <p>No events available</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
