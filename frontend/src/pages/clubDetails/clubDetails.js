import { useState, useEffect, useContext } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import './clubDetails.css';
import Nav from '../../components/nav/nav';

const ClubDetails = () => {
    const { clubId } = useParams();
    const [club_name, setName] = useState([]);
    const [club_description, setDescription] = useState([]);

    const getClubDetails = async () => {
        try{
            const data = await fetch(`/clubs/${clubId}`);
            const clubsData = await data.json();
       
            setName(clubsData.club_name);
            setDescription(clubsData.club_description);
            console.log(club_description)

        }catch{
            console.log("error")
        }
    }

    useEffect(() => {
        getClubDetails();
      }, []);
    

    return (
        <div >
            <div className="main">

           
            <Nav />
            <h1>{club_name}</h1>
            <h3>{club_description}</h3>

            </div>
            <button>Join the groupchat!</button>
        </div>

    );
};

export default ClubDetails;