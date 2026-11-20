import React, { useState, useEffect } from 'react';
import { Plus, RefreshCw, Trash2, CheckCircle2 } from 'lucide-react';
import { getProviders, deleteProvider, refreshProvider, createProvider } from '../services/apiService';

const ProvidersPage = () => {
  const [providers, setProviders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newProvider, setNewProvider] = useState({ name: '', url: '' });

  useEffect(() => {
    fetchProviders();
  }, []);

  const fetchProviders = async () => {
    try {
      setLoading(true);
      const data = await getProviders();
      setProviders(data);
    } catch (error) {
      console.error('Error fetching providers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await createProvider(newProvider);
      setNewProvider({ name: '', url: '' });
      setIsModalOpen(false);
      fetchProviders();
    } catch (error) {
      console.error('Error creating provider:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this provider?')) {
      try {
        await deleteProvider(id);
        fetchProviders();
      } catch (error) {
        console.error('Error deleting provider:', error);
      }
    }
  };

  const handleRefresh = async (id) => {
    try {
      await refreshProvider(id);
      fetchProviders();
    } catch (error) {
      console.error('Error refreshing provider:', error);
    }
  };

  return (
    <div className="p-8 bg-slate-950 min-h-screen text-white">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">IPTV Providers</h1>
          <p className="text-slate-400 mt-2">Manage your upstream IPTV sources and playlists.</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg transition-colors"
        >
          <Plus className="w-5 h-5" />
          Add Provider
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className
            className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"
          ></div>
        </div>
      ) : (
        <div className="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-slate-800/50 text-slate-400 text-sm uppercase">
              <tr>
                <th className="px-6 py-4 font-medium">Name</th>
                <th className="px-6 py-4 font-medium">URL</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {providers.length === 0 ? (
                <tr>
                  <td
                    colSpan={4}
                    className="px-6 py-10 text-center text-slate-500"
                  >
                    No providers found. Add your first source to get started.
                  </td>
                </tr>
              ) : (
                providers.map((provider) => (
                  <tr
                    key={provider.id}
                    className="hover:bg-slate-800/30 transition-colors"
                  >
                    <td className="px-6 py-4 font-medium text-white">
                      {provider.name}
                    </td>
                    <td className="px-6 py-4 text-slate-400 text-sm truncate max-w-xs">
                      {provider.url}
                    </td>
                    <td className="px-6 py-4">
                      <span className="flex items-center gap-2 text-green-400 text-sm">
                        <CheckCircle2 className="w-4 h-4" />
                        Active
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => handleRefresh(provider.id)}
                          className="p-2 hover:bg-slate-700 rounded-lg text-blue-400 transition-colors"
                          title="Refresh Playlist"
                        >
                          <RefreshCw className="w-5 h-5" />
                        </button>
                        <button
                          onClick={() => handleDelete(provider.id)}
                          className="p-2 hover:bg-slate-700 rounded-lg text-red-400 transition-colors"
                          title="Delete Provider"
                        >
                          <Trash2 className:="w-5 h-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {isModalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 w-full max-w-md shadow-2xl">
            <h2 className="text-2xl font-bold mb-6">Add New Provider</h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">
                  Provider Name
                </label>
                <input
                  type="text"
                  required
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                  placeholder="e.g. IPTV Premium"
                  value={newProvider.name}
                  onChange={(e) =>
                    setNewProvider({ ...newProvider, name: e.target.value })
                  }

                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">
                  M3U/HLS URL
                </label>
                <input
                  type="url"
                  required
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                  placeholder="https://example.com/playlist.m3u8"
                  value={newProvider.url}
                  onChange={(e) =>
                    setNewProvider({ ...newProvider, url: e.target.value })
                  }
                />
              </div>
              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(int(false))}
                  className="px-4 py-2 text-slate-400 hover:text-white transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-lg transition-colors"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProvidersPage;
