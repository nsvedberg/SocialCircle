import { useState, useEffect } from 'react';
import './profile.css';
import Nav from '../../components/nav/nav';
import InterestSelector from '../../components/interest/interestSelector';
import { useCurrentUser } from '../../auth/useCurrentUser';

const Profile = () => {
  const { currentUser, setCurrentUser } = useCurrentUser();

  const [formValues, setFormValues] = useState({
    ...currentUser,
    interests: [],
  });

  async function fetchInterest(id) {
    const response = await fetch("/b/interests/" + id);

    var body = await response.json();

    if (response.ok) {
      return body;
    } else {
      console.log("Error fetching interest " + id, body.error);
      console.log(body.message);
    }
  }

  useEffect(() => {
    async function updateInterests() {
      const interests = [];

      for (const id of currentUser.interests) {
        const data = await fetchInterest(id);
        interests.push(data);
      }

      setFormValues((prev) => ({ ...prev, interests }));
    }

    setFormValues({
      ...currentUser,
      interests: []
    });

    updateInterests();
  }, [currentUser]);

  const removeInterest = (id) => {
    setFormValues((prev) => ({
      ...prev,
      interests: prev.interests.filter((elem) => elem.id !== id),
    }));
  }

  const addInterest = async (interest) => {
    setFormValues((prev) => ({
      ...prev,
      interests: prev.interests.concat(interest)
    }))
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    setFormValues({ ...formValues, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = formValues;
    formData.interests = formData.interests.map((x) => x.id);

    const token = currentUser.token;
    
    const response = await fetch("/b/users/" + currentUser.id, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify(formData),
    });

    var body = await response.json();

    if (response.ok) {
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
            value={formValues.email}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='first-name'>First Name:</label>
          <input
            type='text'
            id='first-name'
            name='first_name'
            value={formValues.first_name}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='last-name'>Last Name:</label>
          <input
            type='text'
            id='last-name'
            name='last_name'
            value={formValues.last_name}
            onChange={handleInputChange}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='grad-year'>Year of Graduation:</label>
          <select id='grad-year' name='grad_year'>
            <option>{formValues.grad_year}</option>
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
          <InterestSelector
            interests={formValues.interests}
            addInterest={addInterest}
            removeInterest={removeInterest}/>
        </div>
        <div className='form-group'>
          <label htmlFor='bio'>Bio:</label>
          <textarea
            id='bio'
            name='bio'
            value={formValues.bio}
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
