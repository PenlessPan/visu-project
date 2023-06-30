import streamlit as st

st.set_page_config(page_title="Welcome to Dogly!", layout="centered")
origin_path = r"D:/Users/yaniv/OneDrive - post.bgu.ac.il/studies/university/Information Visualization/project/Project Code/"
image_path = origin_path + r"homepage.jpg"
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
st.write("### You can see all of our dog breeds and explore their attributes or start your searching right away")
st.write("### You are welcome to choose what you would like to do using the sidebar")
st.write("(We recommend to begin with exploring our dogs and then start find your optimal dogs)")
st.write("")  # leave a blank line
st.write("#### Data Overview")
"""
there are 94 dog breeds, and 6 attributes\n
The attributes are: \n
Friendliness, Energy, Protectiveness, Life Expectancy, Size, Maintenance\n
Some of the attributes are actually derived attributes:\n
Friendliness: a mean of the attributes "Good with children", "Good with other dogs" and "Good with strangers"\n
Energy: a mean of the attributes "Energy" and "Playfulness"\n
Life Expectancy:  a mean of the attributes "Min Life Expectancy" and "Max Life Expectancy"\n
Size: a mean of the attributes "Min Height Male", "Max Height Male", "Min Height Female", "Max Height Female"\n
Maintenance: a mean of the attributes "Trainability", "Shedding", "Grooming", "Drooling" and "Barking".
"""

st.sidebar.success("Select a feature from above!")
