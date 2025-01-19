// import React, { useState } from "react";
// import { sendQueryToBackend } from "../api/api";
// import "../styles/chatbot.css";

// const Chatbot = () => {
//   const [messages, setMessages] = useState([]);
//   const [userInput, setUserInput] = useState("");

//   const handleSend = async () => {
//     if (!userInput.trim()) return;

//     // Add user message to the chat
//     const newMessages = [...messages, { role: "user", text: userInput }];
//     setMessages(newMessages);
//     setUserInput("");

//     // Send the query to the backend
//     try {
//       const response = await sendQueryToBackend(userInput);
//     //   console.log(userInput, response);
//       const botMessage = {
//         role: "bot",
//         text: response.data.answer || "I couldn't process that. Please try again.",
//       };
//       setMessages((prev) => [...prev, botMessage]);
//     } catch (error) {
//       const errorMessage = {
//         role: "bot",
//         text: "An error occurred. Please try again later.",
//       };
//       setMessages((prev) => [...prev, errorMessage]);
//     }
//   };

//   return (
//     <div className="chatbot-container">
//       <div className="chat-window">
//         {messages.map((message, index) => (
//           <div
//             key={index}
//             className={`chat-message ${message.role === "user" ? "user" : "bot"}`}
//           >
//             {message.text}
//           </div>
//         ))}
//       </div>
//       <div className="chat-input">
//         <input
//           type="text"
//           value={userInput}
//           onChange={(e) => setUserInput(e.target.value)}
//           placeholder="Type your message here..."
//         />
//         <button onClick={handleSend}>Send</button>
//       </div>
//     </div>
//   );
// };

// export default Chatbot;


import React, { useState } from "react";
import { sendQueryToBackend } from "../api/api";
import "../styles/chatbot.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");

  const handleSend = async () => {
    if (!userInput.trim()) return;
  
    // Add the user's query to the chat history
    const updatedMessages = [...messages, { role: "user", text: userInput }];
    setMessages(updatedMessages);
    setUserInput(""); // Clear the input field
  
    // Debugging: Log the payload being sent
    console.log("Sending query to backend:", { query: userInput, history: updatedMessages });
  
    // Send the query along with chat history to the backend
    try {
      const response = await sendQueryToBackend(userInput, updatedMessages); // Pass the updated history
      console.log("Backend response:", response); // Debugging: Log the backend response
  
      const botMessage = {
        role: "bot",
        text: response.data.answer || "I couldn't process that. Please try again.",
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error occurred:", error); // Debugging: Log the error
      const errorMessage = {
        role: "bot",
        text: "An error occurred. Please try again later.",
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };
  

  return (
    <div className="chatbot-container">
      <div className="chat-window">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`chat-message ${message.role === "user" ? "user" : "bot"}`}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Type your message here..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
