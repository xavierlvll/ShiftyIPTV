import React, { useEffect, useState } from 'react';
import { getStreamEvents } from '../services/apiService';
import { Activity, AlertTriangle, CheckCircle, Clock } from 'lucide-react';

const StatCard = ({ title, value, icon: Icon, colorClass }) => (
  <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-slate-400 text-sm font-medium uppercase tracking-wider">{title}</p>
        <p className="text-2xl font-bold text-white mt-1">{value}</p>
      </div>
      <div className={`p-3 rounded-lg ${colorClass}`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
    </div>
  </div>
);

const Dashboard = () => {
  const [events, setEvents] = `useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
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

    fetchEvents();
    const interval = setInterval(fetchEvents, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-8 bg-slate-900 min-h-screen text-white">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">SHiFTyIPTV Dashboard</h1>
        <p className="text-slate-400 mt-2">Real-time stream monitoring and system health</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard 
          title="Active Streams" 
          value="0" 
          icon={Activity} 
          colorClass="bg-blue-500" 
        />
        <StatCard 
          title="Interruptions" 
          value={events.filter(e => e.event_type.includes('failure')).length} 
          icon={AlertTriangle} 
          colorClass="bg-red-500" 
        />
        <StatCard 
          title="Recoveries" 
          value={events.filter(e => e.event_type.includes('reconnection')).length} 
          icon={CheckCircle} 
          colorClass="bg-green-500" 
        />
        <StatCard 
          title="Last Event" 
          value={events.length > 0 ? 'Recent' : 'None'} 
          icon={Clock} 
          colorClass="bg-slate_500" 
        />
      </div>

      <div className="bg-slate_800 rounded-xl shadow-lg border border-slate_700 overflow-hidden">
        <div className="p-6 border-b border-slate-700">
          <h2 className="text-xl font-semibold">Recent Stream Events</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-700/50 text-slate.300 text-sm uppercase">
              <tr>
                <th className="px-6 py-4 font-medium">Timestamp</th>
                <th className="px-6 py-4 font-medium">Event Type</th>
                <th className="px-6 py-4 font-medium">Description</th>
                <th className="px-6 py-4 font-medium">Channel ID</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700">
              {loading ? (
                <tr>
                  <td colSpan="4" className="px-6 py-10 text-center text-slate-400">
                    Loading event history...
                  </td>
                </tr>
              ) : events.length === 0 ? (
                <tr>
                  <td colSpan="4" className="px-6 py-10 text-center text-slate-400">
                    No recent events recorded.
                  </td>
                </tr>
              ) : (
                events.map((event, idx) => (
                  <tr key={idx} className="hover:bg-slate-700/30 transition-colors">
                    <td className="px-6 py-4 text-slate-300 text-sm">
                      {new Date(event.timestamp).toLocaleTimeString()}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        event.event_type.includes('failure') ? 'bg-red-500/20 text-red-400' :
                        event.event_type.includes('reconnection') ? 'bg-green-500/20 text-green-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>
                        {event.event_type.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-slate-300 text-sm">
                      {event.description}
                    </td>
                    <td className="px-6 py-4 text-slate-400 text-sm">
                      #{event.channel_id}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
