import React, { useState } from "react";
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/home/home';
import Login from './pages/login/login';
import Register from './pages/register/register';
import Dashboard from './pages/dashboard/dashboard'
import Profile from './pages/profile/profile'
import ChatList from './pages/chatList/ChatList';
import Chatbot from './pages/message/Chatbot';
import CreateClub from './pages/club/createClubs';

export const AuthToken = React.createContext(null);

function App() {
  const [token, setToken] = useState(null);

  return (
    <BrowserRouter> 
      <AuthToken.Provider value={{ token: token, setToken: setToken }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/clubs/new" element={<CreateClub />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/chat/:chatId" element={<Chatbot />} />
          <Route path="/messages" element={<ChatList />} />
        </Routes>
      </AuthToken.Provider>
    </BrowserRouter>
  );
}

export default App;
