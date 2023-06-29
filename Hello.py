import streamlit as st

st.set_page_config(page_title="Welcome to Dogly!", layout="centered")

image_path = r"D:\Users\yaniv\OneDrive - post.bgu.ac.il\studies\university\Information Visualization\project\Project Code\homepage.jpg"
st.image(image_path)

# col1, col2, col3 = st.columns([1, 3, 1])
# with col1:
#     st.write(' ')
# with col2:
#     image_path = ""
#     st.image(image_path)
# with col3:
#     st.write(' ')

st.write("# Hello! this system will assist you to find which breeds of dogs to adopt, according to your preferences")
st.write("# Please choose what you would like to do")

st.sidebar.success("Select a feature from above!")

st.markdown(
    """
    dogs are cute!
"""
)