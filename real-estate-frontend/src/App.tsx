// src/App.tsx

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import PropertyList from './components/PropertyList';
import PropertyDetail from './components/PropertyDetail';
import OfferSubmissionForm from './components/OfferSubmission';
import './index.css';


const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Real Estate Platform</h1>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<PropertyList />} />
          <Route path="/property/:id" element={<PropertyDetail />} />
          <Route path="/property/:id/offer" element={<OfferSubmissionForm />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;