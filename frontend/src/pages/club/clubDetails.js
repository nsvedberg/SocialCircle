import { useState, useEffect } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import './clubDetails.css';
import Nav from '../../components/nav/nav';
import { useCurrentUser } from '../../auth/useCurrentUser';

const ClubDetails = () => {
    const { clubId } = useParams();
    const navigate = useNavigate();
    const { currentUser, setCurrentUser } = useCurrentUser();
    
    const [club_name, setName] = useState('');
    const [club_description, setDescription] = useState('');
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState('');
    const [editedComment, setEditedComment] = useState('');
    const [editedCommentId, setEditedCommentId] = useState('');
    const [isEditingClub, setIsEditingClub] = useState(false); 
    const [dropdownOpen, setDropdownOpen] = useState(false); // Dropdown state starts out not open

    // Im using a dropdown for the edit/delete for clubs, this keeps track if its open or not
    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen);
    };

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

    const handleJoinChat = async () => {
        try {
            const response = await fetch(`/b/users/${currentUser.id}/add-to-club/${clubId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const updatedUser = await response.json();
                console.log("Successfully joined the club:", updatedUser);
                alert("You have successfully joined the group chat!");
            } else {
                console.log("Failed to join the club");
                alert("There was an error joining the group chat. Please try again.");
            }
        } catch (error) {
            console.log("Error joining the club:", error);
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

    const deleteComment = async (commentId) => {
        try {
            const response = await fetch(`/b/clubs/${clubId}/comments/${commentId}/delete`, { method: 'DELETE' });
            if (response.ok) {
                alert("Comment deleted successfully");
                window.location.reload(); // Refresh the page and the comment should be gone
            } else {
                console.log("Error deleting comment");
            }
        } catch (error) {
            console.log("Error deleting comment:", error);
        }
    };

    const deleteClub = async () => {
        try {
            const response = await fetch(`/b/clubs/${clubId}`, { method: 'DELETE' });
            if (response.ok) {
                alert("Club deleted successfully");
                navigate('/'); // Redirect to the home
            } else {
                console.log("Error deleting club");
            }
        } catch (error) {
            console.log("Error deleting club:", error);
        }
    };

    const editClub = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`/b/clubs/${clubId}`, {
                method: 'PUT', 
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    club_name, 
                    club_description 
                }),
            });

            if (response.ok) {
                const updatedClub = await response.json();
                setName(updatedClub.club_name);
                setDescription(updatedClub.club_description);
                setIsEditingClub(false); 
            } else {
                console.log("Error editing club");
            }
        } catch (error) {
            console.log("Error editing club:", error);
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
                <div className="dropdown-container">
                    <button className="dropdown-toggle" onClick={toggleDropdown}>
                        Options
                    </button>
                    {dropdownOpen && (
                        <div className="dropdown-menu">
                            <button onClick={() => setIsEditingClub(true)}>Edit Club</button>
                            <button onClick={deleteClub}>Delete Club</button>
                        </div>
                    )}
                </div>
                {isEditingClub ? (
                    <form onSubmit={editClub}>
                        <input
                            type="text"
                            value={club_name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="Club Name"
                            required
                            className="form-input"
                        />
                        <textarea
                            value={club_description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="Club Description"
                            required
                            className="form-input"
                        />
                        <button type="submit">Save</button>
                        <button type="button" onClick={() => setIsEditingClub(false)}>Cancel</button>
                    </form>
                ) : (
                    <>
                        <h1>{club_name}</h1>
                        <h3>{club_description}</h3>
                    </>
                )}
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
                                <button onClick={() => deleteComment(comment.comment_id)}>Delete</button>
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
            <button className="join-chat-btn" onClick={handleJoinChat}>Join the group chat!</button>
        </div>
    );
};

export default ClubDetails;
