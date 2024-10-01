import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    role: ''
  });
  const [notification, setNotification] = useState(''); 
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/auth/register', formData);
      console.log(response.data); 
      navigate('/'); 
    } catch (error) {
      console.error("Registration failed:", error.response?.data || error.message);
      setNotification(error.response?.data?.message || 'Registration failed. Please try again.');
    }
  };

  return (
    <div>
      <h2>Register</h2>
      {notification && <div className="notification">{notification}</div>}
      <form onSubmit={handleRegister}>
        <input type="text" name="first_name" onChange={handleChange} placeholder="First Name" required />
        <input type="text" name="last_name" onChange={handleChange} placeholder="Last Name" required />
        <input type="email" name="email" onChange={handleChange} placeholder="Email" required />
        <input type="password" name="password" onChange={handleChange} placeholder="Password" required />
        <select name="role" onChange={handleChange} required>
          <option value="">Select Role</option>
          <option value="super_admin">Super Admin</option>
          <option value="artist_manager">Artist Manager</option>
          <option value="artist">Artist</option>
        </select>
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
