const ACCESS_TOKEN_KEY = "supportflow_access_token";

export const getAccessToken = () => {
  return localStorage.getItem(
    ACCESS_TOKEN_KEY
  );
};

export const setAccessToken = (
  token
) => {
  localStorage.setItem(
    ACCESS_TOKEN_KEY,
    token
  );
};

export const removeAccessToken = () => {
  localStorage.removeItem(
    ACCESS_TOKEN_KEY
  );
};

export const clearAuthStorage = () => {
  removeAccessToken();
};