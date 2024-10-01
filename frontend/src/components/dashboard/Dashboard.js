import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import UsersTab from './UsersTab';
import ArtistsTab from './ArtistsTab';
import SongsTab from './SongsTab';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('users');
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>
      <button onClick={() => setActiveTab('users')}>Users</button>
      <button onClick={() => setActiveTab('artists')}>Artists</button>
      <button onClick={() => setActiveTab('songs')}>Songs</button>
      <button onClick={handleLogout}>Logout</button>

      {activeTab === 'users' && <UsersTab />}
      {activeTab === 'artists' && <ArtistsTab />}
      {activeTab === 'songs' && <SongsTab />}
    </div>
  );
};

export default Dashboard;
