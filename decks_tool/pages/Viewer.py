import streamlit as st
import streamlit_authenticator as stauth
import yaml
import requests
from yaml.loader import SafeLoader

from utils.auth import get_auth_headers

DECKS_PREVIEW_URL = 'https://us-central1-riddly-98ca6.cloudfunctions.net/getDeckPreviews'
EDIT_DECK_PAGE = "edit_deck.py"  # Page for editing decks
NEW_DECK_PAGE = "new_deck.py"    # Page for creating a new deck

def buttons_markdown():
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
        }

        div.stButton > button:first-child:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

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

if st.session_state.get('authentication_status'):
    # Display logout option
    authenticator.logout(location='sidebar', key='main_logout')

    buttons_markdown()

    # "New" button to create a new deck
    if st.button("Create New Deck", key="new_deck"):
        st.switch_page(f"pages/{NEW_DECK_PAGE}")

    # Get and display deck previews
    response = requests.get(
        DECKS_PREVIEW_URL,
        headers=get_auth_headers(DECKS_PREVIEW_URL)
    )
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            decks = data.get("decks", [])
            if decks:
                st.write("### Available Decks:")
                
                # Iterate over each deck
                for deck in decks:
                    # Create two columns: one for the cover image, the other for the details
                    col1, col2 = st.columns([1, 2])
                    
                    # Deck cover image in the first column
                    with col1:
                        st.image(deck["cover"], width=150)

                    # Deck details in the second column
                    with col2:
                        st.write(f"**Title:** {deck['title']}")
                        st.write(f"**Category:** {deck['category']}")
                        st.write(f"**Summary:** {deck['summary']}")
                        st.write(f"**Price:** ${deck['price']}")
                        st.write(f"**Author:** {deck['author']}")
                        
                        # "Edit" button for each deck
                        if st.button("Edit", key=f"edit_{deck['id']}"):
                            st.session_state['selected_deck'] = deck['id']
                            st.switch_page(f"pages/{EDIT_DECK_PAGE}")

                    # Divider between decks
                    st.markdown("<hr style='border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
            else:
                st.write("No decks available.")
        else:
            st.error("Failed to retrieve decks.")
    else:
        st.error(f"API request failed with status code {response.status_code}.")
else:
    # Display the login form if not authenticated
    st.switch_page("main.py")