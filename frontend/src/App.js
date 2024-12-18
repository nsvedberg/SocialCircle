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
import EventDetails from './pages/event/eventDetails';
import CreateEvent from './pages/event/createEvent';
import Clubs from './pages/club/clubs';
import User from './pages/user/user';
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
          <Route path="/clubs" element={<Clubs />} />
          <Route path="/b/events/new" element={<CreateEvent />} />
          <Route path="/register" element={<Register />} />
          <Route path="/user/:id" element={<User />} />
          <Route path="/dashboard" element={
            <RequireAuth>
              <Dashboard />
            </RequireAuth>
          } />
          <Route path="/profile" element={
            <RequireAuth>
              <Profile />
            </RequireAuth>
          } />
          <Route path="/chat/:chatTitle" element={
            <RequireAuth>
              <Chatbot />
            </RequireAuth>
          } />
          <Route path="/messages" element={
            <RequireAuth>
              <ChatList />
            </RequireAuth>
          } />
          <Route path="/club/:clubId" element={<ClubDetails />} />
          <Route path="/event/:eventId" element={<EventDetails />} />
        </Routes>
      </CurrentUser.Provider>
    </BrowserRouter>
  );
}

export default App;
