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
import streamlit as st
from auth import authenticate, logout, is_authenticated, manage_users
from api import upload_files_to_backend, query_backend, UPLOAD_ENDPOINT, QUERY_ENDPOINT

# Streamlit app configuration
st.set_page_config(page_title="E-commerce Chatbot", layout="wide")

# Global session states for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "Landing"

if "message" not in st.session_state:
    st.session_state["message"] = ""

if "show_sidebar" not in st.session_state:
    st.session_state["show_sidebar"] = True  # Initialize sidebar visibility state

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
    col1, col2,col3=st.columns([8, 1, 1])
    # col1, col2, col3, col4 = st.columns([7, 1, 1, 1])  # Adjust layout for three buttons
    # with col2:
        # if st.button("☰ Toggle Sidebar", key="toggle_sidebar", help="Show/Hide Sidebar", use_container_width=True):
            # toggle_sidebar()
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
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
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

    if "selected_page" in st.session_state and st.session_state["selected_page"] == "Upload Files":
        render_upload_page()
    elif "selected_page" in st.session_state and st.session_state["selected_page"] == "Query System":
        render_query_page()

# Function to render the profile management page
def render_profile_page():
    render_top_bar()
    st.title("Profile Management")
    manage_users()

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
                    data=response.json()
                    st.success("Files uploaded successfully!")
                    # st.write(response.json())
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

    # Initialize chat history if not already set
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []  # Initialize chat history

    # Create a placeholder for chat updates
    chat_placeholder = st.empty()

    # Function to render the chat history dynamically
    def display_chat():
        with chat_placeholder.container():
            for chat in st.session_state["chat_history"]:
                st.markdown(f"**You:** {chat['query']}")
                st.markdown(f"**Bot:** {chat['answer']}")
                st.divider()  # Add a divider between chat messages

    # Display the current chat history
    display_chat()

    # Manage the input field using a placeholder
    # input_placeholder = st.empty()

    # Temporary variable to hold the query
    if "temp_query" not in st.session_state:
        st.session_state["temp_query"] = ""  # Initialize temporary query variable

    # Render the input field in the placeholder
    # with input_placeholder.container():
    #     query = st.text_input(
    #         "Enter your question:",
    #         value=st.session_state["temp_query"],
    #         key="current_query"
    #     )
    # Input field for the current query
    query = st.text_input(
        "Enter your question:",
        value=st.session_state["temp_query"],  # Use the temp_query to persist input
        key="current_query"
    )
    # Submit button for the current query
    if st.button("Send"):
        if query.strip():
            with st.spinner("Fetching answer..."):
                try:
                    # Send query and chat history to the backend
                    response = query_backend(
                        QUERY_ENDPOINT, query, st.session_state["chat_history"]
                    )
                    if response and response.status_code == 200:
                        data = response.json()
                        # Append the new query and answer to chat history
                        st.session_state["chat_history"].append({
                            "query": query,
                            "answer": data.get("answer", "No answer available.")
                        })
                        # Clear the input field indirectly via temp_query
                        st.session_state["temp_query"] = ""
                        # input_placeholder.empty()  # Clear the input placeholder
                        # Re-render the chat with the updated history
                        display_chat()
                    else:
                        st.error(f"Query failed. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"An error occurred during query: {e}")


# Clears the input but have to refresh page to get the response
# def render_query_page():
#     st.title("Chat with the Knowledge Base")

#     # Initialize chat history if not already set
#     if "chat_history" not in st.session_state:
#         st.session_state["chat_history"] = []  # Initialize chat history

#     # Display the chat history dynamically
#     for chat in st.session_state["chat_history"]:
#         st.markdown(f"**You:** {chat['query']}")
#         st.markdown(f"**Bot:** {chat['answer']}")
#         st.divider()  # Add a divider between chat messages

#     # Input field for the current query
#     if "current_query" not in st.session_state:
#         st.session_state["current_query"] = ""  # Initialize query in session state

#     query = st.text_input(
#         "Enter your question:",
#         key="current_query",  # Use a persistent key for the input field
#     )

#     # Submit button for the current query
#     if st.button("Send"):
#         if query.strip():  # Ensure the query is not empty
#             with st.spinner("Fetching answer..."):
#                 try:
#                     # Send query and chat history to the backend
#                     response = query_backend(
#                         QUERY_ENDPOINT, query, st.session_state["chat_history"]
#                     )
#                     if response and response.status_code == 200:
#                         data = response.json()
#                         # Append the new query and answer to chat history
#                         st.session_state["chat_history"].append({
#                             "query": query,
#                             "answer": data.get("answer", "No answer available.")
#                         })
#                         # Clear the input field by resetting the session state variable
#                         st.session_state["current_query"] = ""
#                     else:
#                         st.error(f"Query failed. Status code: {response.status_code}")
#                 except Exception as e:
#                     st.error(f"An error occurred during query: {e}")


def render_profile_page():
    render_top_bar()
    st.title("Profile Management")

    # Button to redirect back to Home Page
    if st.button("Back to Home"):
        st.session_state["page"] = "Home"

    # Clear profile fields on first load
    if "new_user" not in st.session_state or "new_pass" not in st.session_state:
        st.session_state["new_user"] = ""
        st.session_state["new_pass"] = ""

    manage_users()  # Call the `manage_users` function from auth.py

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
