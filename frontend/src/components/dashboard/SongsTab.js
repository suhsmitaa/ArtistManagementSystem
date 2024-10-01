import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const SongsTab = () => {
  const { artistId } = useParams(); 
  const [songs, setSongs] = useState([]);
  const [newSong, setNewSong] = useState({ title: '', genre: '', releaseDate: '' });
  const [editMode, setEditMode] = useState(null);

  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/artists/${artistId}/songs`);
        setSongs(response.data);
      } catch (error) {
        console.error('Failed to fetch songs:', error);
      }
    };

    fetchSongs();
  }, [artistId]);

  const handleCreateSong = async () => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/artists/${artistId}/songs`, newSong);
      setSongs([...songs, response.data]);
      setNewSong({ title: '', genre: '', releaseDate: '' });
    } catch (error) {
      console.error('Failed to create song:', error);
    }
  };

  const handleUpdateSong = async (songId) => {
    try {
      const updatedSong = { ...songs.find(song => song.id === songId), ...newSong };
      const response = await axios.put(`http://127.0.0.1:5000/artists/${artistId}/songs/${songId}`, updatedSong);
      setSongs(songs.map(song => (song.id === songId ? response.data : song)));
      setEditMode(null);
      setNewSong({ title: '', genre: '', releaseDate: '' });
    } catch (error) {
      console.error('Failed to update song:', error);
    }
  };

  const handleDeleteSong = async (songId) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/artists/${artistId}/songs/${songId}`);
      setSongs(songs.filter(song => song.id !== songId));
    } catch (error) {
      console.error('Failed to delete song:', error);
    }
  };

  return (
    <div>
      <h3>Songs for Artist ID: {artistId}</h3>

      <div>
        <h4>{editMode ? 'Edit Song' : 'Add New Song'}</h4>
        <input
          type="text"
          placeholder="Title"
          value={newSong.title}
          onChange={(e) => setNewSong({ ...newSong, title: e.target.value })}
        />
        <input
          type="text"
          placeholder="Genre"
          value={newSong.genre}
          onChange={(e) => setNewSong({ ...newSong, genre: e.target.value })}
        />
        <input
          type="date"
          value={newSong.releaseDate}
          onChange={(e) => setNewSong({ ...newSong, releaseDate: e.target.value })}
        />
        <button onClick={editMode ? () => handleUpdateSong(editMode) : handleCreateSong}>
          {editMode ? 'Update Song' : 'Add Song'}
        </button>
      </div>

      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Genre</th>
            <th>Release Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {songs.map((song) => (
            <tr key={song.id}>
              <td>{song.title}</td>
              <td>{song.genre}</td>
              <td>{new Date(song.releaseDate).toLocaleDateString()}</td>
              <td>
                <button onClick={() => { 
                  setEditMode(song.id); 
                  setNewSong({ title: song.title, genre: song.genre, releaseDate: song.releaseDate });
                }}>
                  Edit
                </button>
                <button onClick={() => handleDeleteSong(song.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SongsTab;
