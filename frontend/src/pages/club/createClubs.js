import { useState, useEffect } from 'react';
import Nav from '../../components/nav/nav';
import { useNavigate } from "react-router-dom";
import './createClub.css';

const CreateClub = () => {
    let navigate = useNavigate();
    const [clubName, setClubName] = useState('');
    const [clubDescription, setClubDescription] = useState('');
    const [clubPresident, setClubPresident] = useState('');
    const [clubEmail, setClubEmail] = useState('');
    const [clubTags, setClubTags] = useState('');
    const [clubMembers, setClubMembers] = useState('');    

    const submit = async (e) => {
        e.preventDefault()

        const data = {
            club_name: clubName,
            club_description: clubDescription,
            club_president: clubPresident,
            club_email: clubEmail,
            club_tags: clubTags,
            club_members: clubMembers,
        }
        const url = "http://127.0.0.1:5000/clubs/new"
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        const response = await fetch(url, options)
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json()
            alert(data.message)
        } else {
            navigate('/dashboard')
        }
    };

    const newClub = {
        club_name: clubName,
        club_description: clubDescription,
        club_president: clubPresident,
        club_email: clubEmail,
        club_tags: clubTags,
        club_members: clubMembers,
    };

    return <form onSubmit={submit}>
        <div>
            <label htmlFor="clubName">Club Name</label>
            <input
                type="text" 
                id="clubName" 
                value={clubName} 
                onChange={(e) => setClubName(e.target.value)}>
            </input>
        </div>
        <div>
            <label htmlFor="clubDescription">Club Description</label>
            <input
                type="text" 
                id="clubDescription" 
                value={clubDescription} 
                onChange={(e) => setClubDescription(e.target.value)}>
            </input>
        </div>
        <div>
            <label htmlFor="clubPresident">Club President</label>
            <input
                type="text" 
                id="clubPresident" 
                value={clubPresident} 
                onChange={(e) => setClubPresident(e.target.value)}>
            </input>
        </div>
        <div>
            <label htmlFor="clubEmail">Club Email</label>
            <input
                type="text" 
                id="clubEmail" 
                value={clubEmail} 
                onChange={(e) => setClubEmail(e.target.value)}>
            </input>
        </div>
        <div>
            <label htmlFor="clubTags">Club Tags</label>
            <input
                type="text" 
                id="clubTags" 
                value={clubTags} 
                onChange={(e) => setClubTags(e.target.value)}>
            </input>
        </div>
        <div>
            <label htmlFor="clubMembers">Club Members</label>
            <input
                type="text" 
                id="clubMembers" 
                value={clubMembers} 
                onChange={(e) => setClubMembers(e.target.value)}>
            </input>
        </div>
        <button type ="submit">Create Club</button>
    </form>
};

export default CreateClub;