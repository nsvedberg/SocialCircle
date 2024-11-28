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

  const handleInputChange = async(event) => {
    const value = event.target.value
    setSearchTerm(value);

    if(value.trim() === ''){
      getEvents();
    } else{
      await handleSearch(value);
    }
  };

  const handleSearch = async (term) => {
    try {
      //searchTerm = JSON.stringify(term)
      //console.log(term)
      //console.log(searchTerm)
      const response = await fetch(`/b/events/name/${term}`);
      const eventData = await response.json();
      setEvents(Array.isArray(eventData) ? eventData : [eventData]); // Ensure data is in array form
    } catch (error) {
      console.error('Error searching for club:', error);
      setEvents([]); // If there's an error, show no clubs
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
