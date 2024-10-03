import { useState, useEffect, useContext } from 'react';
import Nav from '../../components/nav/nav';
import './dashboard.css';
import { AuthToken } from '../../App';

const Dashboard = () => {
  const { token, setToken } = useContext(AuthToken);
  const [clubs, setClubs] = useState([]);

  // Fetch clubs from the backend
  const getClubs = async () => {
    try {
      const data = await fetch("http://127.0.0.1:5000/clubs");
      const clubsData = await data.json();
      console.log(clubsData )
      setClubs(clubsData); // Assuming the data contains a Clubs array
    } catch (error) {
      console.error('Error fetching clubs:', error);
    }
  };

  // Use useEffect to call getClubs when the component loads
  useEffect(() => {
    getClubs();
  }, []);

  return (
    <div className='body'>
      <h1>Clubs</h1>
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
