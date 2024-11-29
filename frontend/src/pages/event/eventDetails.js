import { useState, useEffect, useContext } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import './eventDetails.css';
import Nav from '../../components/nav/nav';
import { CurrentUser } from '../../App';

const EventDetails = () => {
    const { eventId } = useParams();
    const navigate = useNavigate();
    const { currentUser } = useContext(CurrentUser);

    // State variables for event details
    const [event_name, setName] = useState('');
    const [event_description, setDescription] = useState('');
    const [event_location, setLocation] = useState('');
    const [event_time, setTime] = useState('');
    const [event_date, setDate] = useState(''); // New state for event date
    const [isEditingEvent, setIsEditingEvent] = useState(false);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [isRSVPed, setRSVPed] = useState(false);

    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen);
    };

    const getEventDetails = async () => {
        try {
            const response = await fetch(`/b/events/${eventId}`);
            const eventData = await response.json();

            setName(eventData.event_name);
            setDescription(eventData.event_description);
            setLocation(eventData.event_location);
            setTime(eventData.event_time);
            setDate(eventData.event_date); // Set event date
        } catch {
            console.log("Error fetching event details");
        }
    };

    const deleteEvent = async () => {
        try {
            const response = await fetch(`/b/events/${eventId}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                navigate('/');
            } else {
                console.log("Error deleting event");
            }
        } catch (error) {
            console.log("Error deleting event:", error);
        }
    };

    const editEvent = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`/b/events/${eventId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    event_name,
                    event_description,
                    event_location,
                    event_time,
                    event_date, 
                }),
            });

            if (response.ok) {
                const updatedEvent = await response.json();
                setName(updatedEvent.event_name);
                setDescription(updatedEvent.event_description);
                setLocation(updatedEvent.event_location);
                setTime(updatedEvent.event_time);
                setDate(updatedEvent.event_date); 
                setIsEditingEvent(false);
            } else {
                console.log("Error editing event");
            }
        } catch (error) {
            console.log("Error editing event:", error);
        }
    };

    const handleRSVP = async () => {
        try {
            const response = await fetch(`/b/events/${eventId}/rsvp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: currentUser.id,
                }),
            });

            if (response.ok) {
                setRSVPed(true);
            } else {
                console.log("Error RSVPing to the event");
            }
        } catch (error) {
            console.log("Error RSVPing to the event:", error);
        }
    };

    useEffect(() => {
        getEventDetails();
    }, [eventId]);

    return (
        <div className="main">
            <Nav />
            <div className="dropdown-container">
                <button className="dropdown-toggle" onClick={toggleDropdown}>
                    Options
                </button>
                {dropdownOpen && (
                    <div className="dropdown-menu">
                        <button onClick={() => setIsEditingEvent(true)}>Edit Event</button>
                        <button onClick={deleteEvent}>Delete Event</button>
                    </div>
                )}
            </div>
            {isEditingEvent ? (
                <form onSubmit={editEvent}>
                    <input
                        type="text"
                        value={event_name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Event Name"
                        required
                    />
                    <textarea
                        value={event_description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="Event Description"
                        required
                    />
                    <input
                        type="text"
                        value={event_location}
                        onChange={(e) => setLocation(e.target.value)}
                        placeholder="Event Location"
                        required
                    />
                    <input
                        type="date"
                        value={event_date}
                        onChange={(e) => setDate(e.target.value)}
                        placeholder="Event Date"
                        required
                    />
                    <input
                        type="time"
                        value={event_time}
                        onChange={(e) => setTime(e.target.value)}
                        placeholder="Event Time"
                        required
                    />
                    <button type="submit">Save</button>
                    <button type="button" onClick={() => setIsEditingEvent(false)}>Cancel</button>
                </form>
            ) : (
                <>
                    <h1>{event_name}</h1>
                    <p>{event_description}</p>
                    <p>Location: {event_location}</p>
                    <p>Date: {event_date}</p>
                    <p>Time: {event_time}</p>
                    {!isRSVPed ? (
                        <button className="rsvp-button" onClick={handleRSVP}>RSVP</button>
                    ) : (
                        <p>You have successfully RSVPed!</p>
                    )}
                </>
            )}
        </div>
    );
};

export default EventDetails;
