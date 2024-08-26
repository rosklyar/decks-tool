import streamlit as st
import streamlit_authenticator as stauth
import yaml
import requests
from yaml.loader import SafeLoader

from utils.auth import get_auth_headers

DECKS_PREVIEW_URL = 'https://us-central1-riddly-98ca6.cloudfunctions.net/getDeckPreviews'


# Load the authentication configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Set up the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Check if the user is authenticated
if st.session_state.get('authentication_status'):
    # Display logout option
    authenticator.logout(location='sidebar', key='main_logout')

    # Display welcome message
    st.markdown(
        "<h3 style='color: green;'>Welcome to RIDDLY decks management tool</h3>",
        unsafe_allow_html=True
    )

    response = requests.get(
        DECKS_PREVIEW_URL,
        headers=get_auth_headers(DECKS_PREVIEW_URL)
    )

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            decks = data.get("decks", [])
            if decks:
                st.write("Available Decks:")
                for deck in decks:
                    st.image(deck["cover"], width=150)
                    st.write(f"**Title:** {deck['title']}")
                    st.write(f"**Category:** {deck['category']}")
                    st.write(f"**Summary:** {deck['summary']}")
                    st.write(f"**Price:** ${deck['price']}")
                    st.write(f"**Author:** {deck['author']}")
                    st.write("---")
            else:
                st.write("No decks available.")
        else:
            st.error("Failed to retrieve decks.")
    else:
        st.error(f"API request failed with status code {response.status_code}.")
else:
    # Display the login form if not authenticated
    st.switch_page("Main.py")