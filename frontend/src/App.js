import React from 'react';
import './css';
import Upload from './components/Upload';
import ReviewGeneration from './components/ReviewGeneration';
import CitationDisplay from './components/CitationDisplay';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Academic Writing Agent</h1>
      </header>
      <main>
        <Upload />
        <ReviewGeneration />
        <CitationDisplay />
      </main>
    </div>
  );
}

export default App;
