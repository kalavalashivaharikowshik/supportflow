import apiClient from "../api/apiClient";


export const getNotifications = async (
  params = {}
) => {
  const response = await apiClient.get(
    "/notifications",
    {
      params,
    }
  );

  return response.data;
};


export const getUnreadCount = async () => {
  const response = await apiClient.get(
    "/notifications/unread-count"
  );

  return response.data;
};


export const markNotificationRead = async (
  notificationId
) => {
  const response = await apiClient.patch(
    `/notifications/${notificationId}/read`
  );

  return response.data;
};


export const markAllNotificationsRead =
  async () => {
    const response = await apiClient.patch(
      "/notifications/read-all"
    );

    return response.data;
  };