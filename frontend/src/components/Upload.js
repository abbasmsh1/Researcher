import React, { useState } from 'react';
import axios from 'axios';

const Upload = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage('Please select a file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('/api/process-paper', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setMessage(`File uploaded successfully: ${response.data.title}`);
        } catch (error) {
            setMessage('Error uploading file.');
        }
    };

    return (
        <div>
            <h2>Upload Research Paper</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Upload; 