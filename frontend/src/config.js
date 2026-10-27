// Backend URL. Override with REACT_APP_API_URL in frontend/.env
// When the app is served by Flask itself (npm run build), same-origin "" is used.
const API_URL =
  process.env.REACT_APP_API_URL ||
  (window.location.port === "3000" ? "http://127.0.0.1:5000" : "");

export default API_URL;
