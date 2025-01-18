# V1 


# import streamlit as st
# import requests
# from utils.api import upload_files_to_backend, query_backend
# from utils.auth import *

# # API Base URL
# API_BASE_URL = "http://127.0.0.1:8000/"
# API_URL_UPLOAD = f"{API_BASE_URL}/upload"
# API_URL_QUERY = f"{API_BASE_URL}/query"

# # Streamlit App Title
# st.title("E-commerce Chatbot - Admin Panel")

# # Authentication
# if not authenticate():
#     st.stop()

# # Sidebar for Navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to:", ["Upload Files", "Query System"])

# if page == "Upload Files":
#     st.header("File Upload Section")

#     # File Upload Section
#     uploaded_files = st.file_uploader(
#         "Upload files (PDF, TXT, CSV)", 
#         type=["pdf", "txt", "csv"], 
#         accept_multiple_files=True
#     )

#     if uploaded_files:
#         with st.spinner("Uploading files..."):
#             try:
#                 response = upload_files_to_backend(API_URL_UPLOAD, uploaded_files)
#                 if response.status_code == 200:
#                     data = response.json()
#                     st.success("Files processed successfully!")
#                     for file_info in data.get("files", []):
#                         if "message" in file_info:
#                             st.write(f"✅ {file_info['filename']}: {file_info['message']}")
#                         elif "error" in file_info:
#                             st.error(f"❌ {file_info['filename']}: {file_info['error']}")
#                         else:
#                             st.warning(f"⚠️ {file_info['filename']}: Unknown response.")
#                 else:
#                     st.error(f"Failed to process files. Status Code: {response.status_code}")
#             except Exception as e:
#                 st.error(f"An error occurred during file upload: {e}")

# elif page == "Query System":
#     st.header("Query the Knowledge Base")

#     # Query Section
#     query = st.text_input("Enter your question:")
#     if query:
#         with st.spinner("Retrieving answer..."):
#             try:
#                 response = query_backend(API_URL_QUERY, query)
#                 if response.status_code == 200:
#                     data = response.json()
#                     st.write(f"**Query:** {data.get('query', query)}")
#                     st.success(f"**Answer:** {data.get('answer', 'No answer provided.')}")
#                 else:
#                     st.error(f"Failed to retrieve an answer. Status Code: {response.status_code}")
#             except Exception as e:
#                 st.error(f"An error occurred during query: {e}")
