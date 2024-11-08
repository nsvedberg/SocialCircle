import { useState } from 'react';
import './profile.css';
import Nav from '../../components/nav/nav';
import { useCurrentUser } from '../../auth/useCurrentUser';

const Profile = () => {
  let { currentUser, setCurrentUser } = useCurrentUser();

  console.log(currentUser);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    console.log(name);
    console.log(value);
    console.log({
      ...currentUser,
      [name]: value,
    });
    setCurrentUser({
      ...currentUser,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    const token = currentUser.token;

    const response = await fetch("/b/users/" + currentUser.id, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify(Object.fromEntries(formData)),
    });

    var body = await response.json();

    if (response.ok) {
      console.log("Successfully updated profile.");

      body.token = currentUser.token;
      setCurrentUser(body);

    } else {
      console.log("Error updating user " + currentUser.id, body.error);
      console.log(body.message);

      return null
    }
  };

  return (
    <div className='profile-container'>
      <h1>Profile</h1>
      <div className='profile-header'>
        <h2>{currentUser.email}</h2>
      </div>
      <form onSubmit={handleSubmit} className='profile-form'>
        <div className='form-group'>
          <label htmlFor='email'>Email:</label>
          <input
            type='text'
            id='email'
            name='email'
            value={currentUser.email}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='first-name'>First Name:</label>
          <input
            type='text'
            id='first-name'
            name='first_name'
            value={currentUser.first_name}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='last-name'>Last Name:</label>
          <input
            type='text'
            id='last-name'
            name='last_name'
            value={currentUser.last_name}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='grad-year'>Year of Graduation:</label>
          <select id='grad-year' name='grad_year'>
            <option selected="selected">{currentUser.grad_year}</option>
            <option disabled="disabled">--</option>
            <option>2024</option>
            <option>2025</option>
            <option>2026</option>
            <option>2027</option>
            <option>2028</option>
            <option>2029</option>
            <option>2030</option>
          </select>
        </div>
        <div className='form-group'>
          <label htmlFor='interests'>Interests:</label>
          <input
            type='text'
            id='interests'
            name='interests'
            value={currentUser.interests}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='bio'>Bio:</label>
          <textarea
            id='bio'
            name='bio'
            value={currentUser.bio}
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
