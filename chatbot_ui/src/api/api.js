import axios from "axios";

const BASE_URL = "https://e-commerce-chatbot-production.up.railway.app/";

export const sendQueryToBackend = async (query) => {
  return axios.post(`${BASE_URL}/query`, { query });
};
