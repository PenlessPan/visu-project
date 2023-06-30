import streamlit as st

st.set_page_config(page_title="Welcome to Dogly!", layout="centered")
image_path = "homepage.jpg"
st.image(image_path)

st.markdown("""
## Hello! Welcome to Dogly!

### Find Your Ideal Dog Breed!

##### Let Dogly guide you in finding your perfect dog breed. Explore our breeds or start your search right away. Use the sidebar to choose your action.

###### We recommend starting your journey by browsing through the breeds to familiarize yourself with the unique characteristics each breed offers. This will help you better understand your preferences and make an informed decision.

Data Overview: Get to Know Our Dog Breeds

Dogly is home to 94 unique dog breeds, each with its own set of distinctive qualities. To help you make an informed decision, we've categorized each breed based on six key attributes:

- Friendliness: This attribute reflects how well a breed gets along with children, other dogs, and strangers. (Derived from "Good with children," "Good with other dogs," and "Good with strangers")
- Energy: It represents the energy level and playfulness of a breed. (Derived from "Energy" and "Playfulness")
- Protectiveness: This attribute gauges the level of protection a breed provides. (Derived from "Protectiveness")
- Life Expectancy: It provides an estimate of the average lifespan for each breed. (Derived from "Min Life Expectancy" and "Max Life Expectancy")
- Size: This attribute considers the average height of male and female dogs within a breed. (Derived from "Min Height Male," "Max Height Male," "Min Height Female," and "Max Height Female")
- Maintenance: It encompasses trainability, shedding, grooming, drooling, and barking tendencies. (Derived from said features)

We have carefully derived and normalized these attributes to be on a scale from 1 to 5, allowing for easier comparison between breeds.

It's important to note that the attribute ratings are relative only to the breeds within our dataset. For instance, the smallest breed within our dataset will receive a size score of 1, even if smaller breeds exist outside our dataset.

### Feel free to explore the attributes, filter the breeds, and find your ideal companion on Dogly!

""")

st.sidebar.success("Select a feature from above!")
