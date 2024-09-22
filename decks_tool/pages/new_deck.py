import streamlit as st

# Display a form to create a new deck
st.title("Create New Deck")

title = st.text_input("Title")
summary = st.text_area("Summary")
cover = st.text_input("Cover URL")
author = st.text_input("Author")
price = st.number_input("Price", value=0)

# Input section for creating riddles
riddles = []
st.subheader("Add Riddles")
riddle_id = st.text_input("Riddle ID")
riddle_summary = st.text_area("Riddle Summary")
fact = st.text_input("Fact")
hints = st.text_area("Hints (one per line)")
image_hints = st.text_area("Image Hints (one per line)")

if st.button("Add Riddle"):
    riddles.append({
        "id": riddle_id,
        "summary": riddle_summary.splitlines(),
        "fact": fact,
        "hints": hints.splitlines(),
        "imageHints": image_hints.splitlines()
    })
    st.success(f"Riddle '{riddle_id}' added.")

if st.button("Create Deck"):
    new_deck = {
        "title": title,
        "summary": summary,
        "cover": cover,
        "author": author,
        "price": price,
        "riddles": riddles
    }
    # Here, you would send the new deck data to the backend API
    st.success(f"Deck '{title}' created successfully!")
