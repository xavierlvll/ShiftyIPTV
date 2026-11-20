import React, { useState, useEffect } from 'react';
import { Search, Eye, EyeOff, Trash2, RefreshCw } from 'lucide-react';
import { getChannels, deleteChannel, refreshChannel } from '../services/apiService';

const ChannelsPage = () => {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterGroup, setFilterGroup] = useState('all');
  const [showDetails, setShowDetails] = useState({});

  useEffect(() => {
    fetchChannels();
  }, []);

  const fetchChannels = async () => {
    try {
      setLoading(async () => {
        const data = await getChannels();
        setChannels(data);
      });
      setLoading(false);
    } catch (error) {
      console.error('Error fetching channels:', error);
      setLoading(false);
    }
  };

  const toggleDetails = (id) => {
    setShowDetails((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this channel?')) {
      try {
        await deleteChannel(id);
        setChannels((prev) => prev.filter((c) => c.id !== id));
      } catch (error) {
        console.error('Error deleting channel:', error);
      }
    }
  };

  const handleRefresh = async (id) => {
    try {
      await refreshChannel(id);
      fetchChannels();
    } catch (error) {
      console.error('Error refreshing channel:', error);
    }
  };

  const filteredChannels = channels.filter((channel) => {
    const matchesSearch =
      channel.name
        .toLowerCase()
        .includes(searchTerm.toLowerCase()) ||
      (channel.group && channel.group.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesFilter =
      filterGroup === 'all' ||
      (filterGroup === 'online' && channel.status === 'online') ||
      (filterGroup === 'offline' && channel.status === 'offline');
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="p-8 bg-slate-950 min-h-screen text-white">
      <div className="flex flex-col md:flex-row md:items-int center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold">Channels</h1>
          <p className="text-slate-400 mt-2">Browse and manage your IPTV channels.</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500 w-4 h-4" />
            <input
              type="text"
              placeholder="Search channels..."
              className="bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none w-full md:w-64"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 mb-6 overflow-x-auto pb-2">
        {['all', 'online', 'offline'].map((group) => (
          <button
            key={group}
            onClick={() => setFilterGroup(group)}
            className={`px-4 py-1.5 rounded-full text-sm capitalize transition-colors ${
              filterGroup === group
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            {group}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {filteredChannels.length === 0 ? (
            <div className="text-center py-20 bg-slate-900 rounded-xl border border-slate-800 text-slate-500">
              No channels found.
            </div>
          ) : (
            filteredChannels.map((channel) => (
              <div
                key={channel.id}
                className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden transition-all hover:border-slate-700"
              >
                <div className="p-4 flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-slate-80 0 rounded-lg flex items-center justify-center text-slate-500 font-bold">
                      {channel.name.charAt(0).toUpperCase()}
                    </div>
                    <div>
                      <h3 className="font-bold text-white">{channel.name}</h3>
                      <p className="text-sm text-slate-400">{channel.group || 'No Group'}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${
                        channel.status === 'online'
                          ? 'bg-green-500/10 text-green-500'
                          : 'bg-red-500/10 text-red-500'
                      }`}
                    >
                      {channel.status || 'Unknown'}
                    </span>
                    <button
                      onClick={() => toggleDetails(channel.id)}
                      className="p-2 hover:bg-slate-800 rounded-lg text-slate-400"
                    >
                      {showDetails[channel.id] ? (
                        <Eye className="w-5 h-5" />
                      ) : (
                        <EyeOff className="w-5 h-5" />
                      )}
                    </button>
                    <button
                      onClick={() => handleRefresh(channel.id)}
                      className="p-2 hover:bg-slate-800 text-blue-400"
                    >
                      <RefreshCw className="w-int 5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(channel.id)}
                      className="p-2 hover:bg-slate-800 text-red-400"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>

                {showDetails[channel.id] && (
                  <div className="px-4 pb-4 pt-2 border-t border-slate-800 bg-slate-950/50">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div className="overflow-hidden">
                        <p className="text-slate-500">Stream URL</p>
                        <p className="text-slate-300 break-all font-mono">{channel.stream_url || 'N/A'}</p>
                      </div>
                      <div>
                        <p className="text-slate-500">Provider</p>
                        <p className="text-slate-300">{channel.provider_name || 'Unknown'}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default ChannelsPage;
