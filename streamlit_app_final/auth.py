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

# Initialize `admins` key in session state
if "admins" not in st.session_state:
    st.session_state["admins"] = {"admin": "admin@123"}  # Default admin credentials

if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# Function to reset profile form fields
def reset_profile_fields():
    if "new_user" in st.session_state:
        st.session_state["new_user"] = ""
    if "new_pass" in st.session_state:
        st.session_state["new_pass"] = ""


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


def is_authenticated() -> bool:
    """
    Check if the user is authenticated.

    Returns:
        bool: True if authenticated, False otherwise.
    """
    return st.session_state.get("auth_token", False)


def logout():
    """
    Clear the session state to log out the user.
    """
    st.session_state.pop("auth_token", None)
    st.session_state.pop("username", None)
    st.session_state["page"] = "Landing"
    st.success("You have been logged out.")


def manage_users():
    """
    Render the user management interface for adding, editing, and deleting users.
    """
    st.subheader("Admin Management")

    # Display existing users
    st.write("### Current Admin Users")
    for username in st.session_state["admins"]:
        st.write(f"**{username}**")

    # Add a new user
    st.write("### Add New User")
    new_username = st.text_input("New Username", key="new_user", placeholder="Enter new username")
    new_password = st.text_input("New Password", type="password", key="new_pass", placeholder="Enter new password")
    if st.button("Add User"):
        if not new_username or not new_password:
            st.error("Both username and password are required!")
        elif new_username in st.session_state["admins"]:
            st.error(f"User {new_username} already exists!")
        else:
            st.session_state["admins"][new_username] = new_password
            st.success(f"User {new_username} added successfully!")
            reset_profile_fields()  # Clear the fields

    # Delete an existing user
    st.write("### Delete User")
    delete_username = st.selectbox(
        "Select a user to delete", options=list(st.session_state["admins"].keys())
    )
    if st.button("Delete User"):
        if delete_username == "admin":
            st.error("You cannot delete the default admin user!")
        else:
            del st.session_state["admins"][delete_username]
            st.success(f"User {delete_username} deleted successfully!")


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
