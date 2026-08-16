import apiClient from "../api/apiClient";


export const getUsers = async (
  params = {}
) => {
  const response = await apiClient.get(
    "/users",
    {
      params,
    }
  );

  return response.data;
};


export const getUserById = async (
  userId
) => {
  const response = await apiClient.get(
    `/users/${userId}`
  );

  return response.data;
};


export const updateUserStatus = async (
  userId,
  isActive
) => {
  const response =
    await apiClient.patch(
      `/users/${userId}/status`,
      {
        is_active: isActive,
      }
    );

  return response.data;
};


export const updateUserRole = async (
  userId,
  role
) => {
  const response =
    await apiClient.patch(
      `/users/${userId}/role`,
      {
        role,
      }
    );

  return response.data;
};