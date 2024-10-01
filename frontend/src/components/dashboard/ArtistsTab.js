import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ArtistsTab = () => {
  const [artists, setArtists] = useState([]);

  const getToken = () => {
    return localStorage.getItem('token');
  };

  useEffect(() => {
    const fetchArtists = async () => {
      try {
        const token = getToken();
        const response = await axios.get('http://127.0.0.1:5000/artists', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setArtists(response.data);
      } catch (error) {
        console.error('Failed to fetch artists:', error);
      }
    };

    fetchArtists();
  }, []);

  const handleCsvExport = async () => {
    try {
      const token = getToken();
      const response = await axios.get('http://127.0.0.1:5000/artists/export', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: 'blob',
      });
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'artists.csv');
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error('Failed to export CSV:', error);
    }
  };

  const handleCsvImport = async (e) => {
    const formData = new FormData();
    formData.append('file', e.target.files[0]);

    try {
      const token = getToken();
      await axios.post('http://127.0.0.1:5000/artists/import', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Artists imported successfully');
    } catch (error) {
      console.error('Failed to import CSV:', error);
      alert('Failed to import artists.');
    }
  };

  const handleEditArtist = (artistId) => {
    console.log(`Edit artist with ID: ${artistId}`);
  };

  const handleDeleteArtist = async (artistId) => {
    try {
      const token = getToken();
      await axios.delete(`http://127.0.0.1:5000/artists/${artistId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setArtists(artists.filter((artist) => artist.id !== artistId));
      alert('Artist deleted successfully');
    } catch (error) {
      console.error('Failed to delete artist:', error);
      alert('Failed to delete artist.');
    }
  };

  const handleViewSongs = (artistId) => {
    console.log(`View songs for artist with ID: ${artistId}`);
  };

  return (
    <div>
      <h3>Artist Management</h3>

      <button onClick={handleCsvExport}>Export CSV</button>
      <input type="file" onChange={handleCsvImport} accept=".csv" />

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Genre</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {artists.map((artist) => (
            <tr key={artist.id}>
              <td>{artist.name}</td>
              <td>{artist.genre}</td>
              <td>
                <button onClick={() => handleEditArtist(artist.id)}>Edit</button>
                <button onClick={() => handleDeleteArtist(artist.id)}>Delete</button>
                <button onClick={() => handleViewSongs(artist.id)}>View Songs</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ArtistsTab;
