import axios from "axios";

import {
  getAccessToken,
  removeAccessToken,
} from "../utils/storage";


const apiClient = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});


apiClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken();

    if (token) {
      config.headers.Authorization =
        `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);


apiClient.interceptors.response.use(
  (response) => response,

  (error) => {
    if (
      error?.response?.status !== 401
    ) {
      return Promise.reject(error);
    }

    const requestUrl =
      error?.config?.url ?? "";

    const publicAuthRoutes = [
      "/auth/login",
      "/auth/register",
      "/auth/forgot-password",
      "/auth/verify-otp",
      "/auth/reset-password",
    ];

    const isPublicAuthRequest =
      publicAuthRoutes.some(
        (route) =>
          requestUrl.includes(route)
      );

    if (isPublicAuthRequest) {
      return Promise.reject(error);
    }

    const failedAuthorization =
      error?.config?.headers
        ?.Authorization;

    const failedToken =
      failedAuthorization
        ?.toString()
        .replace(
          /^Bearer\s+/i,
          ""
        );

    const currentToken =
      getAccessToken();

    if (
      currentToken &&
      failedToken === currentToken
    ) {
      removeAccessToken();

      window.dispatchEvent(
        new Event(
          "supportflow:unauthorized"
        )
      );
    }

    return Promise.reject(error);
  }
);


export default apiClient;