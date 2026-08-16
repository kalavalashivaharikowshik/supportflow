import apiClient from "../api/apiClient";


export const getAdminConfig =
  async () => {
    const response =
      await apiClient.get(
        "/admin/config"
      );

    return response.data;
  };


export const updateAdminConfig =
  async (
    payload
  ) => {
    const response =
      await apiClient.put(
        "/admin/config",
        payload
      );

    return response.data;
  };