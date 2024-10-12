
import { useState } from 'react';
import './search.css';
import Nav from '../../components/nav/nav';// Sample user data
const users = [
    { name: 'Alice', info: 'Web Developer' },
    { name: 'Bob', info: 'Graphic Designer' },
    { name: 'Charlie', info: 'Data Scientist' },
    { name: 'David', info: 'Software Engineer' },
    { name: 'Eve', info: 'Product Manager' },
];


// Create search wrapper
const searchWrapper = document.createElement('div');
searchWrapper.style.marginBottom = '20px';

// Create search input
const searchInput = document.createElement('input');
searchInput.type = 'text';
searchInput.placeholder = 'Search...';
searchInput.style.width = '100%';
searchInput.style.padding = '10px';
searchInput.style.border = '2px solid #007bff';
searchInput.style.borderRadius = '5px';
searchInput.style.fontSize = '16px';

// Add focus effect
searchInput.addEventListener('focus', () => {
    searchInput.style.borderColor = '#0056b3';
});

// Append search input to search wrapper
searchWrapper.appendChild(searchInput);
document.body.appendChild(searchWrapper);

// Create user cards container
const userCardsContainer = document.createElement('div');
userCardsContainer.style.display = 'grid';
userCardsContainer.style.gridTemplateColumns = 'repeat(auto-fill, minmax(250px, 1fr))';
userCardsContainer.style.gap = '15px';
document.body.appendChild(userCardsContainer);

// Function to render user cards
function renderUserCards(filteredUsers) {
    userCardsContainer.innerHTML = ''; // Clear previous cards

    filteredUsers.forEach(user => {
        const card = document.createElement('div');
        card.style.backgroundColor = '#fff';
        card.style.border = '1px solid #ddd';
        card.style.borderRadius = '8px';
        card.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';
        card.style.padding = '15px';
        card.style.transition = 'transform 0.2s';

        card.onmouseenter = () => {
            card.style.transform = 'scale(1.05)';
        };

        card.onmouseleave = () => {
            card.style.transform = 'scale(1)';
        };

        const header = document.createElement('div');
        header.style.fontSize = '20px';
        header.style.fontWeight = 'bold';
        header.style.marginBottom = '10px';
        header.textContent = user.name;

        const body = document.createElement('div');
        body.style.fontSize = '14px';
        body.style.color = '#555';
        body.textContent = user.info;

        card.appendChild(header);
        card.appendChild(body);
        userCardsContainer.appendChild(card);
    });
}

// Function to filter users based on search input
function filterUsers(event) {
    const searchTerm = event.target.value.toLowerCase();
    const filteredUsers = users.filter(user =>
        user.name.toLowerCase().includes(searchTerm) ||
        user.info.toLowerCase().includes(searchTerm)
    );
    renderUserCards(filteredUsers);
}

// Initial rendering of all user cards
renderUserCards(users);

// Attach event listener to the search input
searchInput.addEventListener('input', filterUsers);
