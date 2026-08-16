import apiClient from "../api/apiClient";


export const getRequesterDashboard =
  async () => {
    const response =
      await apiClient.get(
        "/dashboard/requester"
      );

    return response.data;
  };


export const getAgentDashboard =
  async () => {
    const response =
      await apiClient.get(
        "/dashboard/agent"
      );

    return response.data;
  };


export const getAdminDashboard =
  async () => {
    const response =
      await apiClient.get(
        "/dashboard/admin"
      );

    return response.data;
  };