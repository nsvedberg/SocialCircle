import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './pages/Login/login';

import Register from './pages/register/register';
import Dashboard from './pages/dashboard/dashboard'
import Profile from './pages/profile/profile'
import ChatList from './pages/chatList/ChatList';
import Chatbot from './pages/message/Chatbot';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/chat/:chatId" element={<Chatbot />} />
        <Route path="/messages" element={<ChatList />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
