import streamlit as st

# Function to check user credentials
def check_login(username, password):
    # Retrieve credentials from st.secrets
    users = st.secrets["users"]
    
    # Check if the username exists and password matches
    if username in users and users[username] == password:
        return True
    return False

# Login page function
def login():
    st.title("Login")

    # Create login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # If login button is clicked
    if st.button("Login"):
        # Validate credentials
        if check_login(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# Main function
def main():
    # Check if user is already logged in
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # If not logged in, show login page
    if not st.session_state["logged_in"]:
        login()
    else:
        # If logged in, show the main content
        st.title(f"Welcome {st.session_state['username']}!")
        st.write("This is the main app.")
        if st.button("Logout"):
            st.session_state["logged_in"] = False

# Run the app
if __name__ == "__main__":
    main()
