import { useState } from 'react';
import Nav from '../../components/nav/nav';
import './createEvent.css';
import { useNavigate } from "react-router-dom";

const CreateEvent = () => {
    const [eventName, setEventName] = useState('');
    const [eventDescription, setEventDescription] = useState('');
    const [eventDate, setEventDate] = useState('');
    const [eventTime, setEventTime] = useState('');
    const [eventLocation, setEventLocation] = useState('');
    const [eventClub, setEventClub] = useState('');
    const [eventTags, setEventTags] = useState('');
    const navigate = useNavigate();

    const submit = async (e) => {
        e.preventDefault();

        const data = {
            event_name: eventName,
            event_description: eventDescription,
            event_date: eventDate,
            event_time: eventTime,
            event_location: eventLocation,
            event_club: eventClub,
            event_tags: eventTags,
        };

        const url = "/events/new";
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
            alert('Could not create the event. Please try again.');
        }
    };

    return (
        <div>
            <h1>Create a new event!</h1>
            <Nav />
            <form onSubmit={submit} className="create-event-form">
                <div className="form-group">
                    <label htmlFor="eventName">Event Name</label>
                    <input
                        type="text"
                        id="eventName"
                        value={eventName}
                        onChange={(e) => setEventName(e.target.value)}
                        className="form-input"
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="eventDescription">Event Description</label>
                    <input
                        type="text"
                        id="eventDescription"
                        value={eventDescription}
                        onChange={(e) => setEventDescription(e.target.value)}
                        className="form-input"
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="eventDate">Event Date</label>
                    <input
                        type="date"
                        id="eventDate"
                        value={eventDate}
                        onChange={(e) => setEventDate(e.target.value)}
                        className="form-input"
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="eventTime">Event Time</label>
                    <input
                        type="time"
                        id="eventTime"
                        value={eventTime}
                        onChange={(e) => setEventTime(e.target.value)}
                        className="form-input"
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="eventLocation">Event Location</label>
                    <input
                        type="text"
                        id="eventLocation"
                        value={eventLocation}
                        onChange={(e) => setEventLocation(e.target.value)}
                        className="form-input"
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="eventClub">Event Club</label>
                    <input
                        type="text"
                        id="eventClub"
                        value={eventClub}
                        onChange={(e) => setEventClub(e.target.value)}
                        className="form-input"
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="eventTags">Event Tags</label>
                    <input
                        type="text"
                        id="eventTags"
                        value={eventTags}
                        onChange={(e) => setEventTags(e.target.value)}
                        className="form-input"
                    />
                </div>
                <button type="submit" className="create-event-button">Create Event</button>
            </form>
        </div>
    );
};

export default CreateEvent;
