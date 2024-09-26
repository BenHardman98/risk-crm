import streamlit as st
import yaml

# Load config from YAML file
try:
    with open('config.yaml') as file:
        config = yaml.safe_load(file)
except Exception as e:
    st.error(f"Error loading YAML file: {e}")
# Initialize the authenticator
try:
    authenticator = stauth.Authenticate(
        config['credentials'],
        cookie_name='user_auth',
        cookie_key='auth',
        cookie_expiry_days=30
    )
except Exception as e:
    st.error(f"Error initializing authenticator: {e}")

# User login
name, authentication_status, username = authenticator.login('main')

if authentication_status:
    def homepage_page():
        st.title(f"Welcome, {name}!")
        st.markdown("This is your homepage.")

    def challenge_progression_page():
        st.title(f"Challenge Checks")

    def payout_check_page():
        st.title(f"Payout Checks")

    def adhoc_review_page():
        st.title(f"Adhoc Reviews")

    def spread_trading_page():
        st.title(f"Spread Trading")

    def logout_page():
        st.title(f"Logout")
        # Check if the user is logged out in session state
        if 'logged_out' not in st.session_state:
            st.session_state.logged_out = False

        # If user is not logged out, show confirmation message
        if not st.session_state.logged_out:
            st.write(f"Are you sure you want to log out?")
            # Logout button
            if authenticator.logout('Logout', 'main'):
                # Update session state to reflect the logout
                st.session_state.logged_out = True

        # If the user has logged out, show the goodbye message
        if st.session_state.logged_out:
            st.write(f"Goodbye {name}, you have been logged out.")

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
    selected_page = st.navigation(pages, position="sidebar")

    # Run the selected page
    selected_page.run()

elif authentication_status == False:
    st.error("Username/password is incorrect")

elif authentication_status == None:
    st.warning("Please enter your username and password")

