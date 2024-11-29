import React, { useState, useEffect } from 'react';
import './interestSelector.css';

const Interest = ({data, onRemove}) => {
  return (
    <div className="interest">
      <button onClick={onRemove}>
        <i className="fa-solid fa-xmark"></i>
      </button>
      <span className="interest-name" title={data.description}>{data.name}</span>
      <input type="hidden" name="interests" value={data.id} />
    </div>
  );
}

const InterestMenu = ({ interests, allInterests, addInterest, setShowMenu }) => {
  const buttons = [];

  for (const interest of allInterests) {
    if (interests.map((x) => x.id).includes(interest.id)) {
      continue;
    }

    const callback = (e) => {
      addInterest(interest);
      setShowMenu(false);
    };

    buttons.push(<button type="button" key={interest.id} onClick={callback}>{interest.name}</button>);
  }

  return (
    <div className="add-interest-container">{buttons}</div>
  );
}

const InterestSelector = ({ interests, addInterest, removeInterest }) => {
  const [allInterests, setAllInterests] = useState([]);
  const [showMenu, setShowMenu] = useState(false);

  useEffect(() => {
    async function fetchAllInterests() {
      const response = await fetch("/b/interests");

      var body = await response.json();

      if (response.ok) {
        setAllInterests(body);
      } else {
        console.log("Error fetching all interests", body.error);
        console.log(body.message);
      }
    }

    fetchAllInterests();
  }, []);

  const showMenuCallback = async (e) => {
    setShowMenu(!showMenu);
  }

  return (
    <div className="interest-selector">
      {
        interests.map((data, idx) => 
          <Interest data={data} key={data.id} onRemove={() => removeInterest(data.id)} />)
      }
      <button type="button" onClick={showMenuCallback}>Add Interest</button>
      { showMenu ? <InterestMenu interests={interests} allInterests={allInterests} setShowMenu={setShowMenu} addInterest={addInterest} /> : null }
    </div>
  );
}

export default InterestSelector;
