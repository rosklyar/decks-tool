
import streamlit as st
import requests
from utils.auth import get_auth_headers

DECK_BY_ID_URL = 'https://us-central1-riddly-98ca6.cloudfunctions.net/getDeckById'

# Retrieve the selected deck ID from session state
deck_id = st.session_state.get('selected_deck')

if not deck_id:
    st.error("No deck selected for editing.")
    st.stop()

# Get deck details by ID
response = requests.get(f"{DECK_BY_ID_URL}?deckId={deck_id}", headers=get_auth_headers(DECK_BY_ID_URL))
if response.status_code == 200:
    data = response.json()
    if data.get("success"):
        deck = data.get("deck")

        # Display a form to edit the deck details
        st.title(f"Edit Deck: {deck['title']}")
        
        title = st.text_input("Title", deck['title'])
        summary = st.text_area("Summary", deck['summary'])
        cover = st.text_input("Cover URL", deck['cover'])
        author = st.text_input("Author", deck['author'])
        price = st.number_input("Price", value=deck['price'])

        # Option to edit riddles
        st.subheader("Riddles:")
        for riddle in deck['riddles']:
            with st.expander(f"Edit Riddle: {riddle['id']}"):
                st.text_input(f"Riddle ID: {riddle['id']}", value=riddle['id'], disabled=True)
                st.text_area("Riddle Summary", value="\n".join(riddle['summary']))
                st.text_input("Fact", value=riddle['fact'])
                st.text_area("Hints", value="\n".join(riddle['hints']))
                st.text_area("Image Hints", value="\n".join(riddle['imageHints']))

        if st.button("Save Changes"):
            # Here, you would send the updated data back to the backend API
            st.success(f"Deck '{title}' updated successfully!")
    else:
        st.error("Failed to load the deck.")
else:
    st.error(f"API request failed with status code {response.status_code}.")