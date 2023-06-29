import streamlit as st
import os
st.set_page_config(page_title="Welcome to Dogly!", layout="centered")
image_path = r"homepage.jpg"
st.image(image_path)

# col1, col2, col3 = st.columns([1, 3, 1])
# with col1:
#     st.write(' ')
# with col2:
#     image_path = ""
#     st.image(image_path)
# with col3:
#     st.write(' ')
st.write("# Hello! Dogly will assist you to find which dog breeds to adopt, according to your preferences")
st.write("Here you can see all of our dog breeds and explore their attributes or start your searching right away")
st.write("Please choose what you would like to do using the sidebar")

st.sidebar.success("Select a feature from above!")

st.markdown(
    """
    dogs are cute!
"""
)