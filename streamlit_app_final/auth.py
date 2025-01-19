# # V0

# import streamlit as st

# # Hardcoded admin credentials
# ADMINS = {
#     "admin": "admin@123"
# }

# def is_authenticated() -> bool:
#     """
#     Check if the user is authenticated.
#     """
#     return "auth_token" in st.session_state


# def login_user(username: str, password: str) -> bool:
#     """
#     Authenticate a user based on hardcoded credentials.

#     Args:
#         username (str): The username.
#         password (str): The password.

#     Returns:
#         bool: True if authentication is successful, False otherwise.
#     """
#     if username in ADMINS and ADMINS[username] == password:
#         st.session_state["auth_token"] = True
#         st.session_state["username"] = username
#         return True
#     return False


# def logout():
#     """
#     Clear the session state to log out the user.
#     """
#     st.session_state.pop("auth_token", None)
#     st.session_state.pop("username", None)
#     st.success("You have been logged out.")


# def authenticate():
#     """
#     Render the login page and handle authentication.
#     """
#     st.title("Welcome to E-commerce Chatbot")

#     col1, col2 = st.columns([1, 1])

#     with col1:
#         st.subheader("Login")
#         username = st.text_input("Username", key="login_username")
#         password = st.text_input("Password", type="password", key="login_password")
#         if st.button("Login"):
#             if login_user(username, password):
#                 st.success("Login successful!")
#             else:
#                 st.error("Invalid username or password.")

#     with col2:
#         st.subheader("Register (Disabled)")
#         st.text_input("Username", key="register_username", disabled=True)
#         st.text_input("Password", type="password", key="register_password", disabled=True)
#         st.button("Register", disabled=True)

#     if is_authenticated():
#         st.sidebar.success(f"Logged in as: {st.session_state['username']}")
#         return True

#     return False



# # V3
import streamlit as st

# Initialize session state keys if not already initialized
if "admins" not in st.session_state:
    st.session_state["admins"] = {"admin": "admin@123"}  # Default admin credentials

if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# Authenticate a user based on credentials stored in session state
def authenticate(username: str, password: str) -> bool:
    """
    Authenticate a user based on credentials stored in session state.

    Args:
        username (str): The username.
        password (str): The password.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    admins = st.session_state["admins"]
    if username in admins and admins[username] == password:
        st.session_state["auth_token"] = True
        st.session_state["username"] = username
        return True
    return False

# Check if the user is authenticated
def is_authenticated() -> bool:
    """
    Check if the user is authenticated.

    Returns:
        bool: True if authenticated, False otherwise.
    """
    return st.session_state.get("auth_token", False)

# Log out the user and reset session state
def logout():
    """
    Clear the session state to log out the user.
    """
    st.session_state.pop("auth_token", None)
    st.session_state.pop("username", None)
    st.session_state["page"] = "Landing"
    st.success("You have been logged out.")

# Manage users: Add, delete, or view admin users
def manage_users():
    """
    Render the user management interface for adding, editing, and deleting users.
    """
    st.subheader("Admin Management")

    # Display current admin users
    st.write("### Current Admin Users")
    for username in st.session_state["admins"]:
        st.write(f"**{username}**")

    # Add a new user
    st.write("### Add New User")
    new_user = st.text_input("New Username", key="new_user", placeholder="Enter a new username")
    new_pass = st.text_input("New Password", type="password", key="new_pass", placeholder="Enter a new password")

    if st.button("Add User"):
        if not new_user or not new_pass:
            st.error("Both username and password are required!")
        elif new_user in st.session_state["admins"]:
            st.error(f"User {new_user} already exists!")
        else:
            st.session_state["admins"][new_user] = new_pass
            st.success(f"User {new_user} added successfully!")

    # Delete an existing user
    st.write("### Delete User")
    delete_user = st.selectbox(
        "Select a user to delete", 
        options=list(st.session_state["admins"].keys()), 
        key="delete_user"
    )

    if st.button("Delete User"):
        if delete_user == "admin":
            st.error("You cannot delete the default admin user!")
        else:
            del st.session_state["admins"][delete_user]
            st.success(f"User {delete_user} deleted successfully!")



# V2

# import streamlit as st

# # Hardcoded admin credentials
# ADMINS = {
#     "admin": "admin@123"
# }

# def authenticate(username: str, password: str) -> bool:
#     """
#     Authenticate a user based on hardcoded credentials.

#     Args:
#         username (str): The username.
#         password (str): The password.

#     Returns:
#         bool: True if authentication is successful, False otherwise.
#     """
#     if username in ADMINS and ADMINS[username] == password:
#         st.session_state["auth_token"] = True
#         st.session_state["username"] = username
#         return True
#     return False

# def is_authenticated() -> bool:
#     """
#     Check if the user is authenticated.
#     """
#     return "auth_token" in st.session_state

# def logout():
#     """
#     Clear the session state to log out the user.
#     """
#     st.session_state.pop("auth_token", None)
#     st.session_state.pop("username", None)
#     st.session_state.pop("page", None)
#     st.success("You have been logged out.")
