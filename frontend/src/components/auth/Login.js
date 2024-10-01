import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    password: '',
  });
  const [notification, setNotification] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/auth/login', formData);
      console.log(response.data);
      navigate('/dashboard');
    } catch (error) {
      console.error("Login failed:", error);
      setNotification("Login failed. Please check your credentials or try again later.");
    }
  };

  const handleRegister = () => {
    navigate('/register'); // Navigate to the registration page
  };

  return (
    <div>
      <h2>Login</h2>
      {notification && <div className="notification">{notification}</div>}
      <form onSubmit={handleLogin}>
        <input 
          type="text" 
          name="first_name" 
          onChange={handleChange} 
          placeholder="First Name" 
          required 
        />
        <input 
          type="password" 
          name="password" 
          onChange={handleChange} 
          placeholder="Password" 
          required 
        />
        <button type="submit">Login</button>
      </form>
      <div>
        <p>Don't have an account?</p>
        <button onClick={handleRegister}>Register here</button>
      </div>
    </div>
  );
};

export default Login;
