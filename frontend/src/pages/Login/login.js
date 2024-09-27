
import React, { useState } from "react";
import './login.css' 

import { useNavigate } from 'react-router-dom';


const Login = () => {

    const navigate = useNavigate();
    const [email, setemail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const getUsers = async(email, password) => {
      const data = await fetch("http://localhost:3000/Users")
      const users = await data.json()
      const user = users.find((user) => user.email === email && user.password === password);
      console.log(user)
      return user;
    }

    
  
    const handleSubmit = async(e) => {
      e.preventDefault();
  
      // You can add your authentication logic here
      const isUser = await getUsers(email, password);
      if ( isUser === undefined) {
        console.log("no user")
      } else {
        navigate('/dashboard');
      }
    };


    return (
      <div>
       
        <div className="login-form-container">
          <h2>Login</h2>
          <form onSubmit={handleSubmit}>
            <div>
              <label>email:</label>
              <input
                type="text"
                value={email}
                onChange={(e) => setemail(e.target.value)}
                placeholder="Enter your email"
              />
            </div>
            <div>
              <label>Password:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
              />
            </div>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <button type="submit">Login</button>
            <p>
        Don't have an account yet? <a href="/register">Sign up</a>
      </p>
          </form>
        </div>
      </div>
      );
    };


export default Login;