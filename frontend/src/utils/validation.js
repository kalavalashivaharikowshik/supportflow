export const isValidEmail = (
  email
) => {
  const value = email.trim();

  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
    value
  );
};


export const validatePassword = (
  password
) => {
  if (password.length < 8) {
    return (
      "Password must contain at least " +
      "8 characters."
    );
  }

  return "";
};


export const required = (
  value,
  fieldName
) => {
  if (!String(value ?? "").trim()) {
    return `${fieldName} is required.`;
  }

  return "";
};