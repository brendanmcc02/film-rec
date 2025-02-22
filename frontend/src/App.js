import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import HomePage from './home-page.js';
import RecommendationsPage from './recommendations-page.js';

const App = () => {
  return (
    <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/recommendations-page" element={<RecommendationsPage />} />
        </Routes>
    </BrowserRouter>
  );
};

export default App;
