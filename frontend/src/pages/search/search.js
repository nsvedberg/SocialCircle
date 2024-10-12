import React, { useState } from 'react';
import { useState } from 'react';
import './search.css';

const Search = () => {
// Sample user data
const users = [
    { name: 'Alice', info: 'Web Developer' },
    { name: 'Bob', info: 'Graphic Designer' },
    { name: 'Charlie', info: 'Data Scientist' },
    { name: 'David', info: 'Software Engineer' },
    { name: 'Eve', info: 'Product Manager' },
];

    return(
        <div className = 'searchTitle'>
            <h1>Search Page</h1>
            <div className= 'search-bar'  >
            <input type="text" placeholder="Search..">smile</input>


                </div>  
        </div>

    );

};
export default Search;
