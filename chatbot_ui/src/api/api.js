import axios from "axios";

// const BASE_URL="http://127.0.0.1:8000"
// const BASE_URL = "https://e-commerce-chatbot-production.up.railway.app/";
const BASE_URL="https://e-commerce-chatbot-1-ydcl.onrender.com"

export const sendQueryToBackend = async (query) => {
  const headers = {
    "Content-Type": "application/json",
  };

  const payload = { query };

  return axios.post(`${BASE_URL}/query`, payload, { headers });
};
