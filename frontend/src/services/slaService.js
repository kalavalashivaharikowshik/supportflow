import apiClient from "../api/apiClient";


export const getTicketSlaStatus =
  async (ticketId) => {
    const response =
      await apiClient.get(
        `/tickets/${ticketId}/sla`
      );

    return response.data;
  };


export const getSlaConfigs =
  async () => {
    const response =
      await apiClient.get(
        "/sla/configs"
      );

    return response.data;
  };


export const updateSlaConfig =
  async (
    priority,
    payload
  ) => {
    const response =
      await apiClient.patch(
        `/sla/configs/${priority}`,
        payload
      );

    return response.data;
  };