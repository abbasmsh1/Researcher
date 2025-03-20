import React, { useState } from 'react';
import axios from 'axios';

const PaperUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid PDF file');
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/api/process-paper', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onUploadSuccess(response.data.paper_id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload paper');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="paper-upload">
      <h2>Upload Research Paper</h2>
      <div className="upload-section">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          disabled={loading}
        />
        <button onClick={handleUpload} disabled={!file || loading}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </div>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default PaperUpload; 