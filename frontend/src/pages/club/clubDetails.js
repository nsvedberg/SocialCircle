import { useState, useEffect } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import './clubDetails.css';
import Nav from '../../components/nav/nav';

const ClubDetails = () => {
    const { clubId } = useParams();
    const [club_name, setName] = useState('');
    const [club_description, setDescription] = useState('');
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState('');

    const getClubDetails = async () => {
        try{
            const data = await fetch(`/b/clubs/${clubId}`);
            const clubsData = await data.json();

            setName(clubsData.club_name);
            setDescription(clubsData.club_description);
        } catch {
            console.log("Error fetching club details");
        }
    };

    const getComments = async () => {
        try {
            const response = await fetch(`/b/clubs/${clubId}/comments`);
            const commentsData = await response.json();
            setComments(commentsData);
        } catch {
            console.log("Error fetching comments");
        }
    };

    const addComment = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`/b/clubs/${clubId}/comments`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comment: newComment }),
            });

            if (response.ok) {
                const newCommentData = await response.json();
                setComments([...comments, newCommentData]); 
                setNewComment(''); 
            } else {
                console.log("Error adding comment");
            }
        } catch (error) {
            console.log("Error adding comment:", error);
        }
    };

    useEffect(() => {
        getClubDetails();
        getComments();
    }, [clubId]);

    return (
        <div>
            <div className="main">
                <Nav />
                <h1>{club_name}</h1>
                <h3>{club_description}</h3>
            </div>
            <h4>Comments:</h4>
                <ul>
                    {comments.map((comment) => (
                        <li key={comment.comment_id}>{comment.comment}</li>
                    ))}
                </ul>

                <form className="add-comment-form" onSubmit={addComment}>
                    <input
                        type="text"
                        value={newComment}
                        onChange={(e) => setNewComment(e.target.value)}
                        placeholder="Add a comment"
                        required
                        className="form-input"
                    />
                    <button type="submit">Submit</button>
                </form>
            <button className="join-chat-btn">Join the group chat!</button>
        </div>
    );
};

export default ClubDetails;
