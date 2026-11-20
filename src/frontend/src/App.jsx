import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import ProvidersPage from './pages/Providers';
import ChannelsPage from './pages/Channels';

// Placeholder components for other routes
const Monitoring = () => <div className="p-8 text-white text-2xl">Monitoring Page (Coming Soon)</div>;
const Settings = () => <div className="p-8 text-white text-2xl">Settings Page (Coming Soon)</div>;

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/providers" element={<ProvidersPage />} />
          <Route path="/channels" element={<ChannelsPage />} />
          <Route path="/monitoring" element={<Monitoring />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
