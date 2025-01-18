# V1


# import streamlit as st
# import requests
# from typing import Optional

# # Base URL for authentication endpoints
# API_BASE_URL = "http://127.0.0.1:8000/auth"
# API_URL_LOGIN = f"{API_BASE_URL}/login"
# API_URL_REGISTER = f"{API_BASE_URL}/register"


# def login_user(username: str, password: str) -> Optional[str]:
#     """
#     Authenticate a user and retrieve a JWT token.

#     Args:
#         username (str): The username of the user.
#         password (str): The password of the user.

#     Returns:
#         Optional[str]: JWT token if authentication is successful, None otherwise.
#     """
#     try:
#         response = requests.post(API_URL_LOGIN, json={"username": username, "password": password})
#         if response.status_code == 200:
#             data = response.json()
#             return data.get("access_token")
#         else:
#             st.error(f"Login failed: {response.json().get('detail', 'Unknown error')} ({response.status_code})")
#             return None
#     except Exception as e:
#         st.error(f"An error occurred during login: {e}")
#         return None


# def register_user(username: str, password: str) -> bool:
#     """
#     Register a new user.

#     Args:
#         username (str): The username of the new user.
#         password (str): The password of the new user.

#     Returns:
#         bool: True if registration is successful, False otherwise.
#     """
#     try:
#         response = requests.post(API_URL_REGISTER, json={"username": username, "password": password})
#         if response.status_code == 200:
#             st.success("Registration successful! You can now log in.")
#             return True
#         else:
#             st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')} ({response.status_code})")
#             return False
#     except Exception as e:
#         st.error(f"An error occurred during registration: {e}")
#         return False


# def logout():
#     """
#     Clear the session state to log out the user.
#     """
#     st.session_state.pop("auth_token", None)
#     st.success("You have been logged out.")


# def is_authenticated() -> bool:
#     """
#     Check if the user is authenticated.

#     Returns:
#         bool: True if the user is authenticated, False otherwise.
#     """
#     return "auth_token" in st.session_state


# def authenticate():
#     """
#     Render the login or register UI and handle authentication.
#     """
#     st.sidebar.title("Authentication")
#     auth_option = st.sidebar.radio("Select an option", ["Login", "Register"])

#     if auth_option == "Login":
#         username = st.sidebar.text_input("Username", key="login_username")
#         password = st.sidebar.text_input("Password", type="password", key="login_password")
#         if st.sidebar.button("Login"):
#             token = login_user(username, password)
#             if token:
#                 st.session_state["auth_token"] = token
#                 st.sidebar.success("Login successful!")

#     elif auth_option == "Register":
#         username = st.sidebar.text_input("Username", key="register_username")
#         password = st.sidebar.text_input("Password", type="password", key="register_password")
#         if st.sidebar.button("Register"):
#             register_user(username, password)

#     if is_authenticated():
#         st.sidebar.write(f"Logged in as: {st.session_state.get('login_username', 'Unknown User')}")
#         if st.sidebar.button("Logout"):
#             logout()
#         return True
#     return False
