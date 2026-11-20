import React, { useState, useEffect } from 'react';
import { Search, Eye, EyeOff, Trash2, RefreshCw, MoreVertical, AlertCircle, CheckCircle2, Activity, AlertTriangle, Clock, Terminal } from 'lucide-react';
import { getStreamEvents, clearStreamEvents } from '../services/apiService';

const MonitoringPage = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchEvents = async () => {
    try {
      const data = await getStreamEvents();
      setEvents(data);
    } catch (error) {
      console.error('Error fetching stream events:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async () => {
    if (window.confirm('Are you sure you want to clear all monitoring logs?')) {
      try {
        await clearStreamEvents();
        setEvents([]);
      } catch (error) {
        console.error('Error clearing events:', error);
      }
    }
  };

  const filteredEvents = events.filter((event) => {
    const matchesFilter =
      filter === 'all' ||
      (filter === 'error' && event.type === 'error') ||
      (filter === 'warning' && event.type === 'warning') ||
      (filter === 'info' && event.type === 'info');
    const matchesSearch =
      event.message.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (event.channel_id && event.channel_id.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesFilter && matchesSearch;
  });

  const stats = {
    total: events.length,
    errors: events.filter(e => e.type === 'error').length,
    warnings: events.filter(e => e.type === 'warning').length,
    info: events.filter(e => e.type === 'info').length,
  };

  return (
    <div className="p-8 bg-slate-950 min-h-screen text-white">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold">Stream Monitoring</h1>
          <p className="text-slate-400 mt-2">Real-time analysis of HLS segments and stream health.</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleClear}
            className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors"
          >
            <Terminal className="w-4 h-4" />
            Clear Logs
          </button>
          <button
            onClick={fetchEvents}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between">
            <p className="text-slate-400 text-sm font-medium">Total Events</p>
            <Activity className="text-blue-500 w-5 h-5" />
          </div>
          <p className="text-2xl font-bold mt-2">{stats.total}</p>
        </div>
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between">
            <p className="text-slate-400 text-sm font-medium">Errors</p>
            <AlertTriangle className="text-red-500 w-5 h-5" />
          </div>
          <p className="text-2xl font-bold mt-2 text-red-500">{stats.errors}</p>
        </div>
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between">
            <p className="text-slate-400 text-sm font-medium">Warnings</p>
            <AlertCircle className="text-yellow-500 w-5 h-5" />
          </div>
          <p className="text-2xl font-bold mt-2 text-yellow-500">{stats.warnings}</p>
        </div>
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between">
            <p className="text-slate-400 text-sm font-medium">Info</p>
            <CheckCircle2 className="text-green-500 w-5 h-5" />
          </div>
          <p className="text-2xl font-bold mt-2 text-green-500">{stats.info}</p>
        </div>
      </div>

      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div className="flex items-center gap-2 bg-slate-900 p-1 rounded-lg border border-slate-800 w-fit">
          {['all', 'error', 'warning', 'info'].map((type) => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              className={`px-4 py-1.5 rounded-md text-sm capitalize transition-all ${
                filter === type
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {type}
            </button>
          ))}
        </div>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500 w-4 h-4" />
          <input
            type="text"
            placeholder="Search logs..."
            className="bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none w-full md:w-80"
            value={searchQuery}
            onChange={(e) => setSearchQuery(fmt(e.target.value))}
          />
        </div>
      </div>

      <div className="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden">
        <div className="max-h-[600px] overflow-y-auto">
          {loading ? (
            <div className="p-20 text-center text-slate-500">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
              Loading logs...
            </div>
          ) : filteredEvents.length === 0 ? (
            <div className="p-20 text-center text-slate-500">
              No events found.
            </div>
          ) : (
            <div className="divide-y divide-slate-800">
              {filteredEvents.map((event) => (
                <div key={event.id} className="p-4 hover:bg-slate-800/50 transition-colors">
                  <div className="flex items-start gap-4">
                    <div className={`mt-1 w-2 h-2 rounded-full shrink-0 ${
                      event.type === 'error' ? 'bg-red-500' :
                      event.type === 'warning' ? 'bg-yellow-500' : 'bg-green-500'
                    }`} />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-mono text-slate-50
                        0 uppercase tracking-wider">
                          {new Date(event.timestamp).toLocaleString()}
                        </span>
                        {event.channel_id && (
                          <span className="text-xs bg-blue-500/10 text-blue-500 px-2 py-0.5 rounded font-medium">
                            CH: {event.channel_id}
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-slate-300 mt-1 break-words font-medium">
                        {event.message}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MonitoringPage;
