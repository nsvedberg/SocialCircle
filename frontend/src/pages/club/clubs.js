import { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import './clubs.css';
import CreateButton from '../../components/create/create';
import Nav from '../../components/nav/nav';

const Clubs = () => {
  const [clubs, setClubs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearch = async () => {
    try {
      const response = await fetch(`/b/clubs/name/${searchTerm}`);
      const clubData = await response.json();
      setClubs(Array.isArray(clubData) ? clubData : [clubData]); // Ensure data is in array form
    } catch (error) {
      console.error('Error searching for club:', error);
      setClubs([]);
    }
  };

  const clearBar = async () => {
    setSearchTerm('');
    getClubs();
  };

  const getClubs = async () => {
    try {
      const response = await fetch("/b/clubs");
      const clubsData = await response.json();
      setClubs(clubsData);
    } catch (error) {
      console.error('Error fetching clubs:', error);
    }
  };

  useEffect(() => {
    getClubs();
  }, []);
  

  return (
    <div className='clubs-body'>
      <div className="search-container">
        <input
          type="text"
          value={searchTerm}
          onChange={handleInputChange}
          placeholder="Search..."
          className="search-bar"
        />
        <button onClick={handleSearch} className="search-button">
          Search
        </button>
        <button onClick={clearBar} className="clear-button">
          Clear
        </button>
      </div>

      <CreateButton />
      <Nav />


      <div className="clubs-container">
        {clubs.length > 0 ? (
          clubs.map((club, index) => (
            <div key={index} className="club-card">
              <h2>{club.club_name}</h2>
              <p>Members: {club.Members}</p>
              <a href={`/club/${club.id}`} rel="noopener noreferrer">Visit Club</a>
            </div>
          ))
        ) : (
          <p>No clubs available</p>
        )}
      </div>
    </div>
  );
};

export default Clubs;