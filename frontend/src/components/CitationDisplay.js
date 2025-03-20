import React, { useState } from 'react';
import axios from 'axios';

const CitationDisplay = () => {
    const [paperIds, setPaperIds] = useState('');
    const [style, setStyle] = useState('ieee');
    const [citations, setCitations] = useState([]);
    const [message, setMessage] = useState('');

    const handleGetCitations = async () => {
        if (!paperIds) {
            setMessage('Please enter paper IDs.');
            return;
        }

        try {
            const response = await axios.get(`/api/citations/${style}`, {
                params: { paper_ids: paperIds.split(',') }
            });
            setCitations(response.data.citations);
            setMessage('Citations retrieved successfully.');
        } catch (error) {
            setMessage('Error retrieving citations.');
        }
    };

    return (
        <div>
            <h2>Get Citations</h2>
            <input
                type="text"
                placeholder="Enter paper IDs (comma-separated)"
                value={paperIds}
                onChange={(e) => setPaperIds(e.target.value)}
            />
            <select value={style} onChange={(e) => setStyle(e.target.value)}>
                <option value="ieee">IEEE</option>
                <option value="apa">APA</option>
                <option value="mla">MLA</option>
            </select>
            <button onClick={handleGetCitations}>Get Citations</button>
            {message && <p>{message}</p>}
            {citations.length > 0 && (
                <div>
                    <h3>Citations</h3>
                    <ul>
                        {citations.map((citation, index) => (
                            <li key={index}>{citation}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default CitationDisplay; 