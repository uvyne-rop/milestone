import React, { useState, useEffect } from 'react';
// import axios from 'axios';

const Admin = () => {
    const [spaces, setSpaces] = useState([]);
    const [selectedSpace, setSelectedSpace] = useState(null);
    const [form, setForm] = useState({ name: '', description: '', price: '' });

    // Fetch spaces on component mount
    useEffect(() => {
        fetchSpaces();
    }, []);

    const fetchSpaces = async () => {
        try {
            const response = await axios.get('/api/spaces');
            setSpaces(response.data);
        } catch (error) {
            console.error('Error fetching spaces:', error);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setForm({ ...form, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (selectedSpace) {
                await axios.put(`/api/spaces/${selectedSpace.id}`, form);
            } else {
                await axios.post('/api/spaces', form);
            }
            fetchSpaces();
            setForm({ name: '', description: '', price: '' });
            setSelectedSpace(null);
        } catch (error) {
            console.error('Error saving space:', error);
        }
    };

    const handleEdit = (space) => {
        setSelectedSpace(space);
        setForm(space);
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`/api/spaces/${id}`);
            fetchSpaces();
        } catch (error) {
            console.error('Error deleting space:', error);
        }
    };

    return (
        <div className="admin-page">
            <h1>Manage Spaces</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="name"
                    placeholder="Name"
                    value={form.name}
                    onChange={handleInputChange}
                    required
                />
                <input
                    type="text"
                    name="description"
                    placeholder="Description"
                    value={form.description}
                    onChange={handleInputChange}
                    required
                />
                <input
                    type="number"
                    name="price"
                    placeholder="Price"
                    value={form.price}
                    onChange={handleInputChange}
                    required
                />
                <button type="submit">{selectedSpace ? 'Update' : 'Create'} Space</button>
            </form>
            <h2>Spaces List</h2>
            <ul>
                {spaces.map(space => (
                    <li key={space.id}>
                        <div>{space.name}</div>
                        <div>{space.description}</div>
                        <div>{space.price}</div>
                        <button onClick={() => handleEdit(space)}>Edit</button>
                        <button onClick={() => handleDelete(space.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Admin;
