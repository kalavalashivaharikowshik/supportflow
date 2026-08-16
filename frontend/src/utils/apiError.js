export const getApiErrorMessage = (
  error,
  fallback = "Something went wrong."
) => {
  const data = error?.response?.data;

  if (data?.message) {
    return data.message;
  }

  if (typeof data?.detail === "string") {
    return data.detail;
  }

  if (error?.message) {
    return error.message;
  }

  return fallback;
};

export const getValidationErrors = (
  error
) => {
  const details =
    error?.response?.data?.details;

  if (!Array.isArray(details)) {
    return [];
  }

  return details;
};