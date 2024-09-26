import streamlit as st
import streamlit_authenticator as stauth

# Access the credentials from Streamlit secrets
credentials = st.secrets["credentials"]

# Prepare the credentials in the format required by streamlit_authenticator
try:
    users = {
        'usernames': {
            'user1': {
                'name': credentials['user1']['name'],
                'password': credentials['user1']['password'],
                'accounts': credentials['user1'].get('accounts', [])
            },
            'user2': {
                'name': credentials['user2']['name'],
                'password': credentials['user2']['password'],
                'accounts': credentials['user2'].get('accounts', [])
            },
            'user3': {
                'name': credentials['user3']['name'],
                'password': credentials['user3']['password'],
                'accounts': credentials['user3'].get('accounts', [])
            }
        }
    }

    # Initialize the authenticator with the correct format
    authenticator = stauth.Authenticate(
        users['usernames'],
        cookie_name='user_auth',
        cookie_key='auth',
        cookie_expiry_days=30
    )
except Exception as e:
    st.error(f"Error initializing authenticator: {e}")
    st.stop()  # Stop execution if authenticator initialization fails

# User login
name, authentication_status, username = authenticator.login('main')

if authentication_status:
    # Define pages as you did before
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
        if 'logged_out' not in st.session_state:
            st.session_state.logged_out = False

        if not st.session_state.logged_out:
            st.write(f"Are you sure you want to log out?")
            if authenticator.logout('Logout', 'main'):
                st.session_state.logged_out = True

        if st.session_state.logged_out:
            st.write(f"Goodbye {name}, you have been logged out.")

    # Define pages and sections
    homepage = st.Page(page=homepage_page, title="Homepage", icon=":material/home:")
    challenges = st.Page(page=challenge_progression_page, title="Challenge Progression Checks", icon=":material/query_stats:")
    payouts = st.Page(page=payout_check_page, title="Challenge Payout Checks", icon=":material/mintmark:")
    adhoc = st.Page(page=adhoc_review_page, title="Adhoc Reviews", icon=":material/person_search:")
    spreads = st.Page(page=spread_trading_page, title="Spread Trading", icon=":material/ssid_chart:")
    logout = st.Page(page=logout_page, title="Logout", icon=":material/logout:")

    pages = {
        "Home": [homepage],
        "Tools": [challenges, payouts, adhoc, spreads],
        "Logout": [logout]
    }

    selected_page = st.navigation(pages, position="sidebar")
    selected_page.run()

elif authentication_status == False:
    st.error("Username/password is incorrect")

elif authentication_status == None:
    st.warning("Please enter your username and password")
