import apiClient from "../api/apiClient";


export const register = async (
  payload
) => {
  const response = await apiClient.post(
    "/auth/register",
    payload
  );

  return response.data;
};


export const login = async (
  payload
) => {
  const response = await apiClient.post(
    "/auth/login",
    payload
  );

  return response.data;
};


export const getCurrentUser = async () => {
  const response = await apiClient.get(
    "/auth/me"
  );

  return response.data;
};


export const logout = async () => {
  const response = await apiClient.post(
    "/auth/logout"
  );

  return response.data;
};


export const forgotPassword = async (
  payload
) => {
  const response = await apiClient.post(
    "/auth/forgot-password",
    payload
  );

  return response.data;
};


export const verifyOtp = async (
  payload
) => {
  const response = await apiClient.post(
    "/auth/verify-otp",
    payload
  );

  return response.data;
};


export const resetPassword = async (
  payload
) => {
  const response = await apiClient.post(
    "/auth/reset-password",
    payload
  );

  return response.data;
};


export const updateProfile = async (
  payload
) => {
  const response = await apiClient.patch(
    "/auth/me",
    payload
  );

  return response.data;
};


export const changePassword = async (
  payload
) => {
  const response = await apiClient.post(
    "/auth/change-password",
    payload
  );

  return response.data;
};