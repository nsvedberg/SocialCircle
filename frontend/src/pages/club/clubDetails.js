import { useState, useEffect, useContext } from 'react';
import { useNavigate, useParams, Link } from "react-router-dom";
import './clubDetails.css';
import Nav from '../../components/nav/nav';
import { CurrentUser } from '../../App'
import { useCurrentUser } from '../../auth/useCurrentUser';

const ClubDetails = () => {
    const { clubId } = useParams();
    const navigate = useNavigate();
    const { currentUser, setCurrentUser } = useContext(CurrentUser);
    const [club_name, setName] = useState('');
    const [club_description, setDescription] = useState('');
    const [club_email, setEmail] = useState('');
    const [comments, setComments] = useState([]);
    const [members, setMembers] = useState([]); // User list
    const [newComment, setNewComment] = useState('');
    const [editedComment, setEditedComment] = useState('');
    const [editedCommentId, setEditedCommentId] = useState('');
    const [isEditingClub, setIsEditingClub] = useState(false); 
    const [dropdownOpen, setDropdownOpen] = useState(false); // Dropdown state starts out not open
    const [isCurrentUserCreator, setIsCurrentUserCreator] = useState(false); // This keeps track if the currentUser is the creator or the most senior club member if the creator leaves

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
            setEmail(clubsData.club_email);
            setMembers(clubsData.members);
            setIsCurrentUserCreator(currentUser.id === clubsData.members[0]?.id);
            setUsers(clubsData.users);
        } catch {
            console.log("Error fetching club details");
        }
    };

    const handleJoinChat = async () => {
        try {
            const response = await fetch(`/b/members/${currentUser.id}/add-to-club/${clubId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                getClubDetails(); //refresh club data after user joins
                const updatedUser = await response.json();
                console.log("Successfully joined the club:", updatedUser);
            } else {
                console.log("Failed to join the club");
                alert("There was an error joining the group chat. Please try again.");
            }
        } catch (error) {
            console.log("Error joining the club:", error);
        }
    };

    const handleLeaveChat = async () => {
        try {
            const response = await fetch(`/b/members/${currentUser.id}/remove-from-club/${clubId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                getClubDetails(); //refresh data after user leaves
                const updatedUser = await response.json();
                console.log("Successfully left the club:", updatedUser);
            } else {
                console.log("Failed to leave the club");
                alert("There was an error leaving the club. Please try again.");
            }
        } catch (error) {
            console.log("Error leaving the club:", error);
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
                body: JSON.stringify({ 
                    comment: newComment,
                    creator_id: currentUser.id,
                }),
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
                getComments(); // retreive comments again instead of refreshing the page
                alert("Comment edited successfully");
                // window.location.reload(); // Refresh the page
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
                await getComments(); // retreive comments again instead of refreshing the page
                alert("Comment deleted successfully");
                //window.location.reload(); // Refresh the page and the comment should be gone
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
                    club_description,
                    club_email,
                }),
            });

            if (response.ok) {
                const updatedClub = await response.json();
                setName(updatedClub.club_name);
                setDescription(updatedClub.club_description);
                setEmail(updatedClub.club_email);
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
    <body class="page-specific">
        <div>
            <div className="main">
                <Nav />
                {isCurrentUserCreator && (
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
                </div>)}
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
                        <textarea
                            value={club_email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Club Email"
                            required
                            className="form-input"
                        />
                        <button type="submit">Save</button>
                        <button type="button" onClick={() => setIsEditingClub(false)}>Cancel</button>
                    </form>
                ) : (
                    <> 
                        <h1>{club_name}</h1>
                        <p>{club_description}</p> 
                        <p>Email: {club_email}</p> 
                        <p> 
                            Members:{" "}
                            {members.length > 0 ? ( 
                                members.map((user, index) => ( // Make these users link to the profiles later on
                                    <span key={user.id}> 
                                        {user.first_name} {user.last_name} 
                                        {index < members.length - 1 && ", "}
                                    </span> // ^ Comma after every user, EXCEPT the last one
                                ))
                            ) : (
                                <span>None</span> // Print none if no users in the club
                            )}
                        </p>
                    </>
                )}
            </div>
            <div>
                {members.some(user => user.id === currentUser.id) ?  // If the currentUser is part of the club, then show the leave club option.
                    <button className="leave-chat-btn" onClick={handleLeaveChat}>Leave club</button> :
                    <button className="join-chat-btn" onClick={handleJoinChat}>Join the group chat!</button> // This logic also only shows the join button if the user is not already in club. Fixes error where you could join many times
                }
            </div>
            <div className="comments-container">
                <h4>Comments:</h4>
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
                {comments.map((comment) => (
                    <div key={comment.comment_id} className="comment-card">
                        {editedCommentId === comment.comment_id ? (
                            <form onSubmit={editComment}>
                                <input
                                    type="text"
                                    value={editedComment}
                                    onChange={(e) => setEditedComment(e.target.value)}
                                    placeholder="Edit your comment"
                                    required
                                />
                                <div>
                                    <button type="submit">Save</button>
                                    <button type="button" onClick={() => setEditedCommentId(null)}>Cancel</button>
                                </div>
                            </form>
                        ) : (
                            <>
                                <div className="comment-content">
                                    <span className="comment-author">
                                        <Link to={`/user/${comment.creator_id}`}>{comment.user.first_name} {comment.user.last_name}</Link>
                                    </span>
                                    <span className="comment-text">{comment.comment}</span>
                                </div>
                                {currentUser.id === comment.creator_id && (
                                    <div>
                                        <button onClick={() => {
                                            setEditedCommentId(comment.comment_id);
                                            setEditedComment(comment.comment);
                                        }}>Edit</button>
                                        <button onClick={() => deleteComment(comment.comment_id)}>Delete</button>
                                    </div>
                                )}
                            </>
                        )}
                    </div>
                ))}
            </div>
        </div>
    </body>
    );
};

export default ClubDetails;
