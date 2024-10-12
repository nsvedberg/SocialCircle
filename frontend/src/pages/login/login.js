import React, { useState, useContext } from "react";
import './login.css' 
import { AuthToken } from '../../App';

import { useNavigate, useSearchParams } from 'react-router-dom';


const Login = () => {
  const { token, setToken } = useContext(AuthToken);
  const [searchParams, setSearchParams] = useSearchParams();

  const navigate = useNavigate();

  if (searchParams.get("token")) {
    console.log(searchParams.get("token"));
    setToken(searchParams.get("token"));
    navigate('/dashboard');
  }

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async(e) => {
    e.preventDefault();

    const response = await fetch("/b/login", {
      method: "POST",
      headers: {"content-type": "application/json"},
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    })

    const body = await response.json();

    if (response.ok) {
      setToken(body.data);
      navigate('/dashboard');
    } else {
      setError(body.message);
    }
  };

  return (
    <div>
      <div className="login-form-container">
        <h2>Log In</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Email:</label>
            <input
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
          <button type="submit">Log In</button>
          <a className="btn-oauth" href="/b/authorize/google">
            <img className="oauth-icon" src="/google-oauth.png"></img>
            Sign in with Google
          </a>
          <a className="btn-oauth" href="/b/authorize/github">
            <img className="oauth-icon" src="/github-oauth.png"></img>
            Sign in with GitHub
          </a>
          <p>
            Don't have an account yet? <a href="/register">Sign up</a>
          </p>
        </form>
      </div>
    </div>
  );
};


export default Login;
