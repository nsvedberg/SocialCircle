import { useState, useEffect, useContext } from 'react';
import Nav from '../../components/nav/nav';
import './dashboard.css';
import { AuthToken } from '../../App';
import { useNavigate } from "react-router-dom";
import CreateButton from '../../components/create/create';


const Dashboard = () => {
  const { token, setToken } = useContext(AuthToken);
  const [clubs, setClubs] = useState([]);
  const [currentUser, setCurrentUser] = useState([]);

  const [searchTerm, setSearchTerm] = useState('');

 

  const navigate = useNavigate();

  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearch = async () => {
    try {
      const data = await fetch(`/b/clubs/name/${searchTerm}`);
      const clubData = await data.json();
  
      // If the backend returns a single club object, convert it to an array
      if (clubData) {
        setClubs([clubData]);
      } else {
        setClubs([]); // Clear the clubs array if no club is found
      }
      console.log(clubData);
    } catch (error) {
      console.error('Error searching for club:', error);
      setClubs([]); // In case of error, clear the clubs array
    }
  };

  const clearBar = async () => {
    setSearchTerm("")
    getClubs()
  }
  // Fetch clubs from the backend
  const getClubs = async () => {
    try {
      const data = await fetch("/b/clubs");
      const clubsData = await data.json();
      console.log(clubsData )
      setClubs(clubsData); // Assuming the data contains a Clubs array
    } catch (error) {
      console.error('Error fetching clubs:', error);
    }
  };

  const getCurrentUser = async () => {
    const tok = localStorage.getItem('token');

    try {
      const data = await fetch("/b/current-user", {
        headers: new Headers({
            'Authorization': tok,
        }), 
      });
      const json = await data.json();
      setCurrentUser(json);
    } catch (error) {
      console.error('Error fetching current user:', error);
    }
  };

  // Use useEffect to call getClubs when the component loads
  useEffect(() => {
    if (!token) {
      // TODO: require login on this page
      // navigate('/login');
    }

    getClubs();
    getCurrentUser();
  }, []);

  return (
    
    <div className='body'>



      <div className="login-banner">
        Logged in as {currentUser.email}

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
        
      </div>

      

      <CreateButton />
      <Nav />
      
      {/* Display the clubs in cards */}
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

export default Dashboard;
