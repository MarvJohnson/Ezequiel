export const BASE_URL =
  process.env.VUE_APP_MODE === 'production'
    ? `${window.location.origin}/api/v1/`
    : 'http://localhost:8000/api/v1';
