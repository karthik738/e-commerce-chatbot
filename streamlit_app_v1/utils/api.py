# V1


import requests
import streamlit as st
from typing import List, Optional

# Base API URL
API_BASE_URL = "http://127.0.0.1:8000/"
UPLOAD_ENDPOINT = f"{API_BASE_URL}/upload"
QUERY_ENDPOINT = f"{API_BASE_URL}/query"


def upload_files_to_backend(api_url: str, files: List[st.runtime.uploaded_file_manager.UploadedFile]) -> Optional[requests.Response]:
    """
    Upload files to the backend API.

    Args:
        api_url (str): The upload endpoint URL.
        files (List[UploadedFile]): List of files uploaded via Streamlit's file uploader.

    Returns:
        Optional[requests.Response]: API response object if successful, None otherwise.
    """
    files_to_upload = [("files", (file.name, file.getvalue(), file.type)) for file in files]

    try:
        response = requests.post(api_url, files=files_to_upload)
        if response.status_code == 200:
            return response
        else:
            st.error(f"File upload failed: {response.json().get('detail', 'Unknown error')} (Status Code: {response.status_code})")
            return response
    except Exception as e:
        st.error(f"An error occurred during file upload: {e}")
        return None


def query_backend(api_url: str, query: str) -> Optional[requests.Response]:
    """
    Query the knowledge base through the backend API.

    Args:
        api_url (str): The query endpoint URL.
        query (str): The query string to ask the knowledge base.

    Returns:
        Optional[requests.Response]: API response object if successful, None otherwise.
    """
    try:
        response = requests.post(api_url, json={"query": query})
        if response.status_code == 200:
            return response
        else:
            st.error(f"Query failed: {response.json().get('detail', 'Unknown error')} (Status Code: {response.status_code})")
            return response
    except Exception as e:
        st.error(f"An error occurred during query: {e}")
        return None
