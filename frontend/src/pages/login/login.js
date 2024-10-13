import React, { useState, useContext, useEffect } from "react";
import './login.css' 
import { CurrentUser } from '../../App';

import { useNavigate, useSearchParams } from 'react-router-dom';

const Login = () => {
  const { currentUser, setCurrentUser } = useContext(CurrentUser);
  const [searchParams, setSearchParams] = useSearchParams();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  // Given a username and password, fetch the auth token from the backend.
  const fetchToken = async () => {
    const response = await fetch("/b/login", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    const body = await response.json();

    if (!response.ok) {
      console.log("Error fetching token from /b/login: ", body.message);
      setError("Invalid username or password.");
      return null;
    }

    return body.data;
  }

  // Given an auth token, fetch information about the current user from the backend.
  const fetchCurrentUser = async (token) => {
    const response = await fetch("/b/current-user", {
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
    });

    const body = await response.json();

    if (!response.ok) {
      console.log("Error fetching current user from /b/current-user: ", body.error);
      setError(body.message);

      return null;
    }

    body.token = token;

    return body;
  }

  useEffect(() => {
    // If the user is already logged in, redirect to the dashbaord page.
    if (currentUser) {
      navigate('/dashboard');
    }

    const token = searchParams.get("token");

    if (token) {
      // If we get a token param, we are handling a callback from OAuth login.
      fetchCurrentUser(token).then((user) => {
        if (user) {
          setCurrentUser(user);
          navigate('/dashboard');
        }
      });
    }
  });

  // On submit, attempt to get a login token with the email and password.
  //
  // If that is successful, use the login token to fetch the current user and
  // redirect to the dashboard.
  const handleSubmit = async(e) => {
    e.preventDefault();

    const token = await fetchToken();

    if (!token) {
      return;
    }

    const user = await fetchCurrentUser(token);

    if (user) {
      setCurrentUser(user);
      navigate('/dashboard');
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
