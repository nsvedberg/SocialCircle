import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css"
import './searchEvent.css' 
import { useNavigate } from "react-router-dom";

function SearchEvent() {
    const [startDate, setStartDate] = useState(new Date());
    const navigate = useNavigate();
    return (
        <div className='title-bar'>
            <h1>Event Search</h1>
            <h3>Search by Date</h3>
            <div className='search-container'>
                <DatePicker
                    showIcon
                    selected={startDate}
                    onChange={(date) => setStartDate(date)}
                    dateFormat='MM/DD/YYYY'
                />
            </div>
            <button type='submit'>Submit</button>
        </div>

    );
};


export default SearchEvent