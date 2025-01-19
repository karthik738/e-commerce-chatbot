import axios from "axios";

// Base backend URL
const BASE_URL = "https://e-commerce-chatbot-1-ydcl.onrender.com";

// Function to send query to the backend
export const sendQueryToBackend = async (query, history = []) => {
  try {
    // Prepare the payload
    const payload = {
      query,
      history, // Include chat history if the backend expects it
    };

    // Send the POST request to the backend
    const response = await axios.post(`${BASE_URL}/query`, payload);

    // Check if the response is successful
    if (response.status === 200) {
      return response; // Return the response for further processing
    } else {
      throw new Error(`Unexpected response code: ${response.status}`);
    }
  } catch (error) {
    // Log the error for debugging
    console.error("Error while communicating with the backend:", error);

    // Throw the error to be handled in the calling component
    throw error;
  }
};
