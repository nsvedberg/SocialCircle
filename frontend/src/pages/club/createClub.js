import { useState } from 'react';
import Nav from '../../components/nav/nav';
import './createClub.css';
import { useNavigate } from "react-router-dom";

const CreateClub = () => {
    const [clubName, setClubName] = useState('');
    const [clubDescription, setClubDescription] = useState('');
    const [clubPresident, setClubPresident] = useState('');
    const [clubEmail, setClubEmail] = useState('');
    const [clubTags, setClubTags] = useState('');
    const [clubMembers, setClubMembers] = useState('');
    const navigate = useNavigate();

    const submit = async (e) => {
        e.preventDefault();

        const data = {
            club_name: clubName,
            club_description: clubDescription,
            club_email: clubEmail,
            club_tags: clubTags,
        };

        const url = "/b/clubs/new";
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        };

        try {
            const response = await fetch(url, options);
            if (response.status !== 201 && response.status !== 200) {
                const responseData = await response.json();
                alert(responseData.message);
            } else {
                navigate('/dashboard');
            }
        } catch (error) {
            console.error('Error submitting the form:', error);
            alert('Could not create the club. Please try again.');
        }
    };

    return (
        <div>
            <h1>Create a new club!</h1>
            <Nav />
        <form onSubmit={submit} className="create-club-form">
            <div className="form-group">
                <label htmlFor="clubName">Club Name</label>
                <input
                    type="text"
                    id="clubName"
                    value={clubName}
                    onChange={(e) => setClubName(e.target.value)}
                    className="form-input"
                />
            </div>
            <div className="form-group">
                <label htmlFor="clubDescription">Club Description</label>
                <input
                    type="text"
                    id="clubDescription"
                    value={clubDescription}
                    onChange={(e) => setClubDescription(e.target.value)}
                    className="form-input"
                />
            </div>
            <div className="form-group">
                <label htmlFor="clubEmail">Club Email</label>
                <input
                    type="text"
                    id="clubEmail"
                    value={clubEmail}
                    onChange={(e) => setClubEmail(e.target.value)}
                    className="form-input"
                />
            </div>
            <div className="form-group">
                <label htmlFor="clubTags">Club Tags</label>
                <input
                    type="text"
                    id="clubTags"
                    value={clubTags}
                    onChange={(e) => setClubTags(e.target.value)}
                    className="form-input"
                />
            </div>
            <button type="submit" className="create-club-button">Create Club</button>
        </form>
        </div>
    );
};

export default CreateClub;
