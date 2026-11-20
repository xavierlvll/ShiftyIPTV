import apiClient from './apiClient';

export const getProviders = async () => {
  const response = await apiClient.get('/providers');
  return response.data;
};

export const createProvider = async (providerData) => {
  const response = await apiClient.post('/providers', providerData);
  return response.data;
};

export const deleteProvider = async (providerId) => {
  const response = await apiClient.delete(`/providers/${providerId}`);
  return response.data;
};

export const refreshProvider = async (providerId) => {
  const response = await apiClient.post(`/providers/${providerId}/refresh`);
  return response.data;
};

export const importProvider = async (providerId) => {
  const response = await apiClient.post(`/providers/${providerId}/import`);
  return response.data;
};

export const getChannels = async () => {
  const response = await apiClient.get('/channels');
  return response.data;
};

export const getStreamEvents = async (channelId = null) => {
  const url = channelId ? `/monitoring/events?channel_id=${channelId}` : '/monitoring/events';
  const response = await apiClient.get(url);
  return response.data;
};

export const clearStreamEvents = async (channel_id = null) => {
  const url = channelId ? `/monitoring/events/clear?channel_id=${channelId}` : '/monitoring/events/clear';
  const response = await apiClient.post(url);
  return response.data;
};

export const getSettings = async () => {
  const response = await apiClient.get('/settings');
  return response.data;
};

export const updateSettings = async (settingsData) => {
  const response = await apiClient.put('/settings', settingsData);
  return response.data;
};
