import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';

// Placeholder components for other routes
const Providers = () => <div className="p-8 text-white text-2xl">Providers Page (Coming Soon)</div>;
const Channels = () => <div className="p-8 text-white text-2xl">Channels Page (Coming Soon)</div>;
const Monitoring = () => <div className="p-8 text-white text-2xl">Monitoring Page (Coming Soon)</div>;
const Settings = () => <div className="p-8 text-white text-2xl">Settings Page (Coming Soon)</div>;

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/providers" element={<Providers />} />
          <Route path="/channels" element={<Channels />} />
          <Route path="/monitoring" element={<Monitoring />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
