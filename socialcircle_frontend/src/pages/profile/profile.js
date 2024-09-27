import { useState } from 'react';
import './profile.css';
import Nav from '../../components/nav/nav';

const Profile = () => {
  const [profile, setProfile] = useState({
    username: '',
    profilePicture: '',
    interests: '',
    preferredClubTypes: '',
    favoriteActivities: '',
    bio: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfile((prevProfile) => ({
      ...prevProfile,
      [name]: value,
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfile((prevProfile) => ({
          ...prevProfile,
          profilePicture: reader.result,
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission, e.g., send data to server
    console.log('Profile updated:', profile);
  };

  return (
    <div className='profile-container'>
      <h1>Profile</h1>
      <div className='profile-header'>
        <img
          src={profile.profilePicture || 'default-profile-pic.png'}
          alt='Profile'
          className='profile-picture'
        />
        <input
          type='file'
          accept='image/*'
          onChange={handleImageChange}
          className='file-input'
        />
        <h2>{profile.username || 'alanka'}</h2>
      </div>
      <form onSubmit={handleSubmit} className='profile-form'>
        <div className='form-group'>
          <label htmlFor='username'>Username:</label>
          <input
            type='text'
            id='username'
            name='username'
            value={profile.username}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='interests'>Interests:</label>
          <input
            type='text'
            id='interests'
            name='interests'
            value={profile.interests}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='preferredClubTypes'>Preferred Club Types:</label>
          <input
            type='text'
            id='preferredClubTypes'
            name='preferredClubTypes'
            value={profile.preferredClubTypes}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='favoriteActivities'>Favorite Activities:</label>
          <input
            type='text'
            id='favoriteActivities'
            name='favoriteActivities'
            value={profile.favoriteActivities}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='bio'>Bio:</label>
          <textarea
            id='bio'
            name='bio'
            value={profile.bio}
            onChange={handleInputChange}
          ></textarea>
        </div>
        <button type='submit' className='submit-button'>Save Changes</button>
      </form>
      <Nav />
    </div>
  );
};

export default Profile;
