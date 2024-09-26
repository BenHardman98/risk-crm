import streamlit as st
import pandas as pd

# Set page configuration to wide mode
st.set_page_config(layout="wide")
st.logo('FooterLogo.png')

def homepage_page():
    # Access the user's name from session state
    name = st.session_state.get("name", "User")
    st.title(f"Welcome, {name}!")
    st.markdown("This is your homepage.")

def challenge_progression_page():
    st.title("Challenge Progression Checks")
    # Initialize connection.
    conn = st.connection('mysql', type='sql')

    # Perform query.
    df = conn.query('SELECT * FROM mytable;', ttl=600)

    st.dataframe(df)

def payout_check_page():
    st.title("Payout Checks")

def adhoc_review_page():
    st.title("Adhoc Reviews")

def spread_trading_page():
    st.title("Spread Trading")

def logout_page():
    st.title("Logout")
    # Check if the user is logged out in session state
    if 'logged_out' not in st.session_state:
        st.session_state.logged_out = False

    # If user is not logged out, show confirmation message
    if not st.session_state.logged_out:
        st.write("Are you sure you want to log out?")
        if st.button("Confirm Logout"):
            st.session_state["logged_in"] = False
            st.session_state["logged_out"] = True
            st.success("Logged out successfully!")

# Define pages with icons using st.Page
homepage = st.Page(page=homepage_page, title="Homepage", icon=":material/home:")
challenges = st.Page(page=challenge_progression_page, title="Challenge Progression Checks", icon=":material/query_stats:")
payouts = st.Page(page=payout_check_page, title="Challenge Payout Checks", icon=":material/mintmark:")
adhoc = st.Page(page=adhoc_review_page, title="Adhoc Reviews", icon=":material/person_search:")
spreads = st.Page(page=spread_trading_page, title="Spread Trading", icon=":material/ssid_chart:")
logout = st.Page(page=logout_page, title="Logout", icon=":material/logout:")

# Group pages into sections
pages = {
    "Home": [homepage],
    "Tools": [challenges, payouts, adhoc, spreads],
    "Logout": [logout]  # Logout page added here
}

# Create the navigation menu
def create_navigation():
    selected_page = st.navigation(pages, position="sidebar")
    # Run the selected page
    selected_page.run()

# Function to check user credentials
def check_login(username, password):
    # Retrieve credentials from st.secrets
    users = st.secrets["users"]

    # Check if the username exists and password matches
    for user, details in users.items():
        if details["username"] == username and details["password"] == password:
            return details["name"]
    return None

# Login page function
def login():
    st.title("Login")

    # Create login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # If login button is clicked
    if st.button("Login"):
        # Validate credentials and retrieve name
        name = check_login(username, password)
        
        # Check if credentials are valid
        if name:
            st.session_state["logged_in"] = True
            st.session_state["name"] = name
            st.success(f"Logged in successfully as {name}!")
            
            # Redirect to the homepage by setting session state
            st.session_state["current_page"] = "Home"
            st.rerun()
        else:
            # Show error message when login fails
            st.error("Incorrect username or password. Please try again.")

# Main function
def main():
    # Check if user is already logged in
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # If not logged in, show login page
    if not st.session_state["logged_in"]:
        login()
    else:
        # If logged in, create the navigation and show pages
        create_navigation()

# Run the app
if __name__ == "__main__":
    main()
