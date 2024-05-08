import React from 'react';
import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './home.js';
import Recs from './recs.js';

const App = () => {
  return (
    <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/recs" element={<Recs />} />
        </Routes>
    </BrowserRouter>
  );
};

export default App;
