# # V0

# import streamlit as st
# from auth import authenticate, logout, is_authenticated
# from api import upload_files_to_backend, query_backend, UPLOAD_ENDPOINT,QUERY_ENDPOINT

# # Streamlit app title
# st.set_page_config(page_title="E-commerce Chatbot", layout="wide")

# # Authentication
# if not authenticate():
#     st.stop()

# # Navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to:", ["Upload Files", "Query System"])

# # Logout button in the top right
# if st.sidebar.button("Logout"):
#     logout()
#     st.experimental_rerun()

# # Upload Files Page
# if page == "Upload Files":
#     st.header("File Upload Section")
#     uploaded_files = st.file_uploader(
#         "Upload files (PDF, TXT, CSV) - Max 10 MB",
#         type=["pdf", "txt", "csv"],
#         accept_multiple_files=True
#     )

#     if uploaded_files:
#         with st.spinner("Uploading files..."):
#             response = upload_files_to_backend(UPLOAD_ENDPOINT, uploaded_files)
#             if response and response.status_code == 200:
#                 st.success("Files uploaded successfully!")
#                 # st.write(response.json())
#             else:
#                 st.error("File upload failed.")

# # Query System Page
# elif page == "Query System":
#     st.header("Query the Knowledge Base")
#     query = st.text_input("Enter your question:")
#     if query:
#         with st.spinner("Fetching answer..."):
#             response = query_backend(QUERY_ENDPOINT, query)
#             if response and response.status_code == 200:
#                 st.success(response.json().get("answer", "No answer available."))
#             else:
#                 st.error("Query failed.")



# # V3 
# V3
import streamlit as st
from auth import authenticate, logout, is_authenticated, manage_users
from api import upload_files_to_backend, query_backend, UPLOAD_ENDPOINT, QUERY_ENDPOINT

# Streamlit app configuration
st.set_page_config(page_title="E-commerce Chatbot", layout="wide")

# Initialize session state
session_keys = {
    "page": "Landing",
    "message": "",
    "show_sidebar": True,
    "selected_page": "Upload Files",
    "new_user": "",
    "new_pass": "",
    "chat_history": [],
    "temp_query": "",
    "login_username": "",
    "login_password": "",
    "auth_token": False,
    "admins": {"admin": "admin@123"},  # Default admin credentials
}
for key, default_value in session_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# Function to toggle the sidebar
def toggle_sidebar():
    st.session_state["show_sidebar"] = not st.session_state["show_sidebar"]

# Logout button in the top right
def render_top_bar():
    st.markdown(
        """
        <style>
        .top-right-button {
            position: absolute;
            top: 10px;
            right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([8, 1, 1])
    with col2:
        if st.button("Profile", key="profile", help="Manage profile and users", use_container_width=True):
            st.session_state["page"] = "Profile"
    with col3:
        if st.button("Logout", key="logout", help="Log out of your session", use_container_width=True):
            logout()
            st.session_state["page"] = "Landing"

# Function to render the landing page
def render_landing_page():
    st.title("Welcome to E-commerce Chatbot")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        if st.button("Login"):
            if authenticate(username, password):
                st.success("Login successful!")
                st.session_state["page"] = "Home"
            else:
                st.error("Invalid username or password.")

    with col2:
        st.subheader("Register (Disabled)")
        st.text_input("Username", key="register_username", disabled=True)
        st.text_input("Password", type="password", key="register_password", disabled=True)
        st.button("Register", disabled=True)

# Function to render the home page with navigation
def render_home_page():
    render_top_bar()
    if st.session_state["show_sidebar"]:
        st.sidebar.title("Navigation")
        st.session_state["selected_page"] = st.sidebar.radio(
            "Go to:", ["Upload Files", "Query System"], index=0
        )

    if st.session_state["selected_page"] == "Upload Files":
        render_upload_page()
    elif st.session_state["selected_page"] == "Query System":
        render_query_page()

# Upload Files page
def render_upload_page():
    st.title("File Upload Section")
    uploaded_files = st.file_uploader(
        "Upload files (PDF, TXT, CSV) - Max 10 MB",
        type=["pdf", "txt", "csv"],
        accept_multiple_files=True
    )

    if uploaded_files:
        with st.spinner("Uploading files..."):
            try:
                response = upload_files_to_backend(UPLOAD_ENDPOINT, uploaded_files)
                if response and response.status_code == 200:
                    data = response.json()
                    st.success("Files uploaded successfully!")
                    for file_info in data.get("files", []):
                        if "message" in file_info:
                            st.write(f"✅ {file_info['filename']}: {file_info['message']}")
                        elif "error" in file_info:
                            st.error(f"❌ {file_info['filename']}: {file_info['error']}")
                        else:
                            st.warning(f"⚠️ {file_info['filename']}: Unknown response.")
                else:
                    st.error("File upload failed.")
            except Exception as e:
                st.error(f"An error occurred during file upload: {e}")

# Query System page
def render_query_page():
    st.title("Chat with the Knowledge Base")

    def display_chat():
        for chat in st.session_state["chat_history"]:
            st.markdown(f"**You:** {chat['query']}")
            st.markdown(f"**Bot:** {chat['answer']}")
            st.divider()

    display_chat()

    query = st.text_input("Enter your question:", key="temp_query", placeholder="Type your question here...")
    if st.button("Send"):
        if query.strip():
            with st.spinner("Fetching answer..."):
                try:
                    response = query_backend(QUERY_ENDPOINT, query, st.session_state["chat_history"])
                    if response and response.status_code == 200:
                        data = response.json()
                        st.session_state["chat_history"].append({
                            "query": query,
                            "answer": data.get("answer", "No answer available.")
                        })
                        st.session_state["temp_query"] = ""  # Clear the input field
                    else:
                        st.error(f"Query failed. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"An error occurred during query: {e}")

# Profile Management page
def render_profile_page():
    render_top_bar()
    st.title("Profile Management")
    manage_users()

# Main App Logic
if st.session_state["page"] == "Landing":
    render_landing_page()
elif st.session_state["page"] == "Home":
    render_home_page()
elif st.session_state["page"] == "Profile":
    render_profile_page()


# V2 

# import streamlit as st
# from auth import authenticate, logout, is_authenticated
# from api import upload_files_to_backend, query_backend,UPLOAD_ENDPOINT,QUERY_ENDPOINT

# # Streamlit app configuration
# st.set_page_config(page_title="E-commerce Chatbot", layout="wide")

# # Global session states for navigation
# if "page" not in st.session_state:
#     st.session_state["page"] = "Landing"

# # Logout button in the top right
# def render_logout():
#     st.markdown(
#         """
#         <style>
#         .logout-button {
#             position: absolute;
#             top: 10px;
#             right: 10px;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
#     if st.button("Logout", key="logout", help="Log out of your session", use_container_width=False):
#         logout()
#         st.session_state["page"] = "Landing"

# # Function to render the landing page
# def render_landing_page():
#     st.title("Welcome to E-commerce Chatbot")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Login")
#         username = st.text_input("Username", key="login_username")
#         password = st.text_input("Password", type="password", key="login_password")
#         if st.button("Login"):
#             if authenticate(username, password):
#                 st.success("Login successful")
#                 st.session_state["page"] = "Home"
#             else:
#                 st.error("Invalid username or password.")

#     with col2:
#         st.subheader("Register (Disabled)")
#         st.text_input("Username", key="register_username", disabled=True)
#         st.text_input("Password", type="password", key="register_password", disabled=True)
#         st.button("Register", disabled=True)

# # Function to render the home page with navigation
# def render_home_page():
#     render_logout()
#     st.sidebar.title("Navigation")
#     st.session_state["selected_page"] = st.sidebar.radio(
#         "Go to:", ["Upload Files", "Query System"], index=0
#     )

#     if st.session_state["selected_page"] == "Upload Files":
#         render_upload_page()
#     elif st.session_state["selected_page"] == "Query System":
#         render_query_page()

# # Upload Files page
# def render_upload_page():
#     st.title("File Upload Section")
#     uploaded_files = st.file_uploader(
#         "Upload files (PDF, TXT, CSV) - Max 10 MB",
#         type=["pdf", "txt", "csv"],
#         accept_multiple_files=True
#     )

#     if uploaded_files:
#         with st.spinner("Uploading files..."):
#             response = upload_files_to_backend(UPLOAD_ENDPOINT, uploaded_files)
#             if response and response.status_code == 200:
#                 st.success("Files uploaded successfully!")
#                 # st.write(response.json())
#             else:
#                 st.error("File upload failed.")

# # Query System page
# def render_query_page():
#     st.title("Query the Knowledge Base")
#     query = st.text_input("Enter your question:")
#     if query:
#         with st.spinner("Fetching answer..."):
#             response = query_backend(QUERY_ENDPOINT, query)
#             if response and response.status_code == 200:
#                 st.success(response.json().get("answer", "No answer available."))
#             else:
#                 st.error("Query failed.")

# # Main App Logic
# if st.session_state["page"] == "Landing":
#     render_landing_page()
# elif st.session_state["page"] == "Home":
#     render_home_page()
