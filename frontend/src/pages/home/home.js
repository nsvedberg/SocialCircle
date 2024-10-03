import React from "react";
import './home.css'

import { Navigate } from 'react-router-dom';


const Home = () => {
  return (
    <Navigate to="/dashboard" replace={true} />
  );
};


export default Home;
