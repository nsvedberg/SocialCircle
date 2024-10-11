import React from 'react';
import { Link } from 'react-router-dom';
import './create.css'; 
import { useNavigate } from 'react-router-dom';

// Button that sends to the create club page
const CreateButton = () => {
    let navigate = useNavigate();

    const sendToCreate = () => {
        navigate('/clubs/new');
    };

    return (
        <div className="button-container"> 
            <h1>Clubs</h1>
            <button className="create-button" onClick={sendToCreate}>+</button>
        </div>
    );
};

export default CreateButton;