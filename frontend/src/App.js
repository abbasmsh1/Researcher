import React from 'react';
import './App.css';
import Upload from './components/Upload';
import ReviewGenerator from './components/ReviewGenerator';
import CitationDisplay from './components/CitationDisplay';

function App() {
  return (
    <div className="App">
      <div className="container">
        <h1>Research Paper Assistant</h1>
        
        <section className="upload-container">
          <h2>Upload Papers</h2>
          <Upload />
        </section>

        <section className="review-section">
          <h2>Generate Review</h2>
          <ReviewGenerator />
        </section>

        <section className="citation-section">
          <h2>Citation Management</h2>
          <CitationDisplay />
        </section>
      </div>
    </div>
  );
}

export default App;
