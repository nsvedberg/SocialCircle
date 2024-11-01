import { useState, useEffect } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import './clubDetails.css';
import Nav from '../../components/nav/nav';

const ClubDetails = () => {
    const { clubId } = useParams();
    const navigate = useNavigate();
    
    const [club_name, setName] = useState('');
    const [club_description, setDescription] = useState('');
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState('');
    const [editedComment, setEditedComment] = useState('')
    const [editedCommentId, setEditedCommentId] = useState('')

    const getClubDetails = async () => {
        try {
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

    const editComment = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`/b/clubs/${clubId}/comments/${editedCommentId}/edit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comment: editedComment }),
            });

            if (response.ok) {
                const updatedComment = await response.json();
                setComments(comments.map(comment =>
                    comment.comment_id === editedCommentId ? updatedComment : comment
                ));
                setEditedCommentId(null);
                setEditedComment('');
            } else {
                console.log("Error editing comment");
            }
        } catch (error) {
            console.log("Error editing comment:", error);
        }
    };

    const deleteClub = async () => {
        try {
            const response = await fetch(`/b/clubs/${clubId}`, { method: 'DELETE' });
            if (response.ok) {
                alert("Club deleted successfully");
                navigate('/'); // Redirect to the home page or any other relevant page
            } else {
                console.log("Error deleting club");
            }
        } catch (error) {
            console.log("Error deleting club:", error);
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
                <button className = "delete" onClick={deleteClub}>
                    Delete Club
                </button>
                <h1>{club_name}</h1>
                <h3>{club_description}</h3>
            </div>
            <h4>Comments:</h4>
            <ul>
                {comments.map((comment) => (
                    <li key={comment.comment_id}>
                        {editedCommentId === comment.comment_id ? (
                            <form onSubmit={editComment}>
                                <input
                                    type="text"
                                    value={editedComment}
                                    onChange={(e) => setEditedComment(e.target.value)}
                                    placeholder="Edit your comment"
                                    required
                                    className="form-input"
                                />
                                <button type="submit">Save</button>
                                <button type="button" onClick={() => setEditedCommentId(null)}>Cancel</button>
                            </form>
                        ) : (
                            <>
                                <span>{comment.comment}</span>
                                <button onClick={() => {
                                    setEditedCommentId(comment.comment_id);
                                    setEditedComment(comment.comment);
                                }}>Edit</button>
                            </>
                        )}
                    </li>
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
