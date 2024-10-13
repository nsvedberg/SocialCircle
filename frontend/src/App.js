import React, { useState } from "react";
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/home/home';
import Login from './pages/login/login';
import Logout from './pages/logout/logout';
import Register from './pages/register/register';
import Dashboard from './pages/dashboard/dashboard'
import Profile from './pages/profile/profile'
import ChatList from './pages/chatList/ChatList';
import Chatbot from './pages/message/Chatbot';
import CreateClub from './pages/club/createClub';
import ClubDetails from './pages/club/clubDetails';
import CreateEvent from './pages/event/createEvent';
import { useCurrentUser, RequireAuth } from './auth/useCurrentUser'

export const CurrentUser = React.createContext(null);

function App() {
  const { currentUser, setCurrentUser } = useCurrentUser();

  return (
    <BrowserRouter> 
      <CurrentUser.Provider value={{ currentUser, setCurrentUser }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/clubs/new" element={<CreateClub />} />
          <Route path="/events/new" element={<CreateEvent />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={
            <RequireAuth>
              <Dashboard />
            </RequireAuth>
          } />
          <Route path="/profile" element={<Profile />} />
          <Route path="/chat/:chatId" element={<Chatbot />} />
          <Route path="/messages" element={<ChatList />} />
          <Route path="/club/:clubId" element={<ClubDetails />} />
        </Routes>
      </CurrentUser.Provider>
    </BrowserRouter>
  );
}

export default App;
