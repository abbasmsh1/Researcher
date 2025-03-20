import React, { useState } from 'react';
import axios from 'axios';

const ReviewGeneration = () => {
    const [paperIds, setPaperIds] = useState('');
    const [topic, setTopic] = useState('');
    const [review, setReview] = useState(null);
    const [message, setMessage] = useState('');

    const handleGenerateReview = async () => {
        if (!paperIds || !topic) {
            setMessage('Please enter paper IDs and a topic.');
            return;
        }

        try {
            const response = await axios.post('/api/generate-review', {
                papers: paperIds.split(','),
                topic: topic
            });
            setReview(response.data);
            setMessage('Review generated successfully.');
        } catch (error) {
            setMessage('Error generating review.');
        }
    };

    return (
        <div>
            <h2>Generate Review</h2>
            <input
                type="text"
                placeholder="Enter paper IDs (comma-separated)"
                value={paperIds}
                onChange={(e) => setPaperIds(e.target.value)}
            />
            <input
                type="text"
                placeholder="Enter topic"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
            />
            <button onClick={handleGenerateReview}>Generate Review</button>
            {message && <p>{message}</p>}
            {review && (
                <div>
                    <h3>{review.title}</h3>
                    <p>{review.abstract}</p>
                    <h4>Introduction</h4>
                    <p>{review.introduction.content}</p>
                    <h4>Methodology</h4>
                    <p>{review.methodology.content}</p>
                    <h4>Results</h4>
                    <p>{review.results.content}</p>
                    <h4>Discussion</h4>
                    <p>{review.discussion.content}</p>
                    <h4>Conclusion</h4>
                    <p>{review.conclusion.content}</p>
                </div>
            )}
        </div>
    );
};

export default ReviewGeneration; 