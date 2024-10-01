import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UsersTab = () => {
    const [users, setUsers] = useState([]);
    const [newUser, setNewUser] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        role: ''
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false); 

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        setLoading(true); 
        try {
            const response = await axios.get('http://127.0.0.1:5000/users/');
            console.log('Fetched Users:', response.data);
            setUsers(response.data);
        } catch (err) {
            console.error('Error fetching users:', err);
            if (err.response && err.response.status === 403) {
                setError('You are not authorized to view this page');
            } else {
                setError('Failed to fetch users');
            }
        } finally {
            setLoading(false); 
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewUser({
            ...newUser,
            [name]: value
        });
    };

    const handleCreateUser = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
    
        try {
            const response = await axios.post('http://127.0.0.1:5000/users/register', newUser);
            console.log('Response status:', response.status);
            console.log('Response data:', response.data);
    
            if (response.status === 201) {
                setSuccess(response.data.message);
                setNewUser({
                    first_name: '',
                    last_name: '',
                    email: '',
                    password: '',
                    role: ''
                });
                fetchUsers(); // Refresh user list
            } else {
                setError('User creation failed');
            }
        } catch (err) {
            console.error('Error creating user:', err);
            if (err.response && err.response.data) {
                setError(err.response.data.message);
            } else {
                setError('No response received');
            }
        }
    };
    

    return (
        <div>
            <h2>Users</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {success && <p style={{ color: 'green' }}>{success}</p>}
            <form onSubmit={handleCreateUser}>
                <label>
                    First Name:
                    <input
                        type="text"
                        name="first_name"
                        placeholder="First Name"
                        value={newUser.first_name}
                        onChange={handleInputChange}
                        required
                    />
                </label>
                <label>
                    Last Name:
                    <input
                        type="text"
                        name="last_name"
                        placeholder="Last Name"
                        value={newUser.last_name}
                        onChange={handleInputChange}
                        required
                    />
                </label>
                <label>
                    Email:
                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        value={newUser.email}
                        onChange={handleInputChange}
                        required
                    />
                </label>
                <label>
                    Password:
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        value={newUser.password}
                        onChange={handleInputChange}
                        required
                    />
                </label>
                <label>
                    Role:
                    <select
                        name="role"
                        value={newUser.role}
                        onChange={handleInputChange}
                        required
                    >
                        <option value="">Select Role</option>
                        <option value="super_admin">Super Admin</option>
                        <option value="admin">Admin</option>
                        <option value="user">User</option>
                    </select>
                </label>
                <button type="submit">Create User</button>
            </form>
            {loading ? ( 
                <p>Loading users...</p>
            ) : (
                <>
                    <h3>User List</h3>
                    {users.length === 0 ? (
                        <p>No users found</p>
                    ) : (
                        <ul>
                            {users.map(user => (
                                <li key={user.id}>
                                    {user.first_name} {user.last_name} - {user.email} ({user.role})
                                </li>
                            ))}
                        </ul>
                    )}
                </>
            )}
        </div>
    );
};

export default UsersTab;
