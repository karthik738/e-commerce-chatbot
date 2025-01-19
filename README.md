---

# **E-commerce Chatbot**

A robust, embeddable chatbot designed for eCommerce websites to enhance customer engagement and optimize customer acquisition. This chatbot uses a **Retrieval-Augmented Generation (RAG)** pipeline to answer user queries based on uploaded files such as product catalogs, FAQs, and other resources.

---

## **Features**

### 1. **File Upload for RAG Pipeline**
- Upload files in formats such as PDF, TXT, or CSV.
- Automatically processes files and integrates them into the chatbot's knowledge base.

### 2. **Customer Engagement**
- Handles user queries based on the knowledge base.
- Allows follow-up questions with conversational context retained.
- Provides concise and accurate answers to user queries.

### 3. **Embeddable Chat Interface**
- User-friendly chat interface for integration into any eCommerce website.
- Easily embeddable using a React-based frontend.

---

## **Demo**

### **Deployed Links**
- **Streamlit Admin Panel**: [Streamlit App](https://e-commerce-chatbot.streamlit.app/)
- **React Chatbot Interface**: [Vercel Deployment](https://e-commerce-chatbot-black.vercel.app/)
- **Backend API Test**: [Render Deployment](https://e-commerce-chatbot-3wi8.onrender.com/)

### **Screenshots**

   ![Image 1](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1250).png?raw=true)

   ![Image 2](![./images/Screenshot%20(1300).png](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1251).png?raw=true))

   ![Image 3](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1258).png?raw=true)

   ![Image 4](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1259).png?raw=true)

   ![Image 5](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1260).png?raw=true)

   ![Image 6](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1261).png?raw=true)

   ![Image 7](![./images/Screenshot%20(1300).png](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1262).png?raw=true))

   ![Image 8](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1264).png?raw=true)

   ![Image 9](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1265).png?raw=true)

   ![Image 10](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1266).png?raw=true)


   ![Image 11](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1267).png?raw=true)

   ![Image 12](![./images/Screenshot%20(1300).png](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1268).png?raw=true))

   ![Image 13](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1269).png?raw=true)

   ![Image 14](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1270).png?raw=true)

   ![Image 15](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1271).png?raw=true)

   ![Image 16](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1272).png?raw=true)

   ![Image 17](![./images/Screenshot%20(1300).png](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1273).png?raw=true))

   ![Image 18](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1292).png?raw=true)

   ![Image 19](https://github.com/karthik738/e-commerce-chatbot/blob/main/images/Screenshot%20(1293).png?raw=true)


---

## **Setup and Deployment**

### **1. Clone the Repository**
```bash
git clone https://github.com/karthik738/e-commerce-chatbot
cd e-commerce-chatbot
```

### **2. Backend Setup**

#### Prerequisites:
- Python 3.8+
- Pinecone API Key

#### Install dependencies:
```bash
pip install -r requirements.txt
```

#### Configuration:
1. **Pinecone Setup**:
   Set your Pinecone API key and environment in the `backend/main.py` file or as environment variables:
   ```bash
   export PINECONE_API_KEY=<your_api_key>
   export PINECONE_ENVIRONMENT=<your_environment>
   ```

2. **Run the Backend**:
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

---

### **3. Streamlit Frontend (Admin Panel)**

#### Prerequisites:
- Install Streamlit:
  ```bash
  pip install streamlit
  ```

#### Run the App:
```bash
cd streamlit_app_final
streamlit run app.py
```

---

### **4. Chatbot UI (React Interface)**

#### Prerequisites:
- Node.js and npm/yarn installed.

#### Steps:
1. Navigate to the `chatbot_ui` directory:
   ```bash
   cd chatbot_ui
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure API Endpoint:
   Update the `BASE_URL` in `api.js` to point to your backend's deployment URL:
   ```javascript
   const BASE_URL = "https://e-commerce-chatbot-3wi8.onrender.com/";
   ```

4. Start the Development Server:
   ```bash
   npm start
   ```

5. Deploy the Chatbot UI:
   Use **Vercel** for deployment:
   ```bash
   npm install -g vercel
   vercel deploy
   ```

---

## **Architecture**

### **Retrieval-Augmented Generation (RAG) Pipeline**

1. **File Upload**: Files uploaded via Streamlit are processed and indexed into Pinecone.
2. **Query Handling**:
   - When a user asks a question, the chatbot retrieves relevant chunks from Pinecone.
   - Uses a language model (LLM) to generate answers based on the retrieved context.
3. **Answer Delivery**: The chatbot sends back concise and relevant answers.

---

## **Embedding Process**

### For the React-based Chatbot UI:

1. Deploy the chatbot to a service like **Vercel**.
2. Copy the provided embed script:
   ```html
   <iframe
     src="https://e-commerce-chatbot-black.vercel.app/"
     width="400"
     height="600"
     style="border:none;"
   ></iframe>
   ```
3. Add the iframe to your eCommerce website's HTML.

---

## **File Structure**

```plaintext
ecommerce-chatbot/
│
├── backend/                 # Backend API with FastAPI
│   ├── main.py              # Entry point for the backend
│   ├── services/            # File processing and embedding logic
│   └── requirements.txt     # Backend dependencies
│
├── streamlit_app_final/     # Streamlit admin interface
│   ├── app.py               # Entry point for Streamlit app
│   └── utils/               # Utility functions for file upload and query
│
├── chatbot_ui/              # React-based chatbot interface
│   ├── src/
│   ├── public/
│   └── package.json         # React dependencies
│
└── README.md                # Documentation
```

---

## **FAQs**

1. **Can the chatbot handle follow-up queries?**  
   Yes, it retains conversational history for seamless follow-ups.

2. **How is the knowledge base updated?**  
   Upload updated files via the admin panel to refresh the knowledge base.

3. **What file formats are supported?**  
   PDF, TXT, and CSV.

---

## **Contributing**
We welcome contributions! Please create a pull request or open an issue for any improvements or bugs.

---

## **License**
This project is licensed under the MIT License. See `LICENSE` for details.

---

