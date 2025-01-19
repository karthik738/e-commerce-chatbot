import axios from "axios";

// const BASE_URL="http://127.0.0.1:8000"
// const BASE_URL = "https://e-commerce-chatbot-production.up.railway.app/";
const BASE_URL="https://e-commerce-chatbot-3wi8.onrender.com"

export const sendQueryToBackend = async (query) => {
  return axios.post(`${BASE_URL}/query`, { query });
};
