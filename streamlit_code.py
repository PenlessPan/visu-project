import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
import os
df = pd.read_csv('./dog_breeds.csv')
df = df.drop(df[df['drooling'] == 0].index, inplace=False)
attributes = pd.DataFrame()
attributes['Maintenance'] = (df['shedding'] + df['grooming'] + df['drooling'] + df['trainability'] + df['barking']) / 5
attributes['Friendliness'] = (df['good_with_children'] + df['good_with_other_dogs'] + df['good_with_strangers']) / 3
attributes['Energy'] = (df['energy'] + df['playfulness']) / 2
attributes['life_expectancy'] = (df['max_life_expectancy'] + df['min_life_expectancy']) / 2
attributes['Protectiveness'] = df['protectiveness']

temp = pd.DataFrame()
temp['height'] = ((df['max_height_male'] + df['min_height_male']) / 2 + (df['max_height_female'] + df['min_height_female']) / 2) / 2
temp['weight'] = ((df['max_weight_male'] + df['min_weight_male']) / 2 + (df['max_weight_female'] + df['min_weight_female']) / 2) / 2
temp['coat_length'] = df['coat_length']
scaler = MinMaxScaler()
temp[['height', 'weight', 'coat_length']] = (scaler.fit_transform(temp[['height', 'weight', 'coat_length']]) * 4) + 1

attributes['Appearance'] = (temp['height'] + temp['weight'] + temp['coat_length']) / 3

# Set up the dog breed pictures directory
img_dir = "./dog_pics"

# Define the available attributes
attribute_names = ['Maintenance', 'Friendliness', 'Energy', 'Life Expectancy', 'Protectiveness', 'Appearance']

# Define the attribute range for filtering
attribute_ranges = {
    'Maintenance': [1, 5],
    'Friendliness': [1, 5],
    'Energy': [1, 5],
    'Life Expectancy': [1, 5],
    'Protectiveness': [1, 5],
    'Appearance': [1, 5]
}

# Filter breeds based on attribute thresholds
def filter_breeds(data, attribute_filters):
    mask = (data >= attribute_filters[:, 0]) & (data <= attribute_filters[:, 1])
    return data[mask.all(axis=1)]

# Sidebar - Breed Selection
st.sidebar.title("Dog Breed Selection")

# Display the dog breed table
st.sidebar.subheader("Dog Breed Table")
breed_selected = st.sidebar.selectbox("Select a breed", df['Name'])

# Display the selected breed image
image_path = os.path.join(img_dir, breed_selected + ".png")
if os.path.exists(image_path):
    st.sidebar.image(image_path, use_column_width=True)
else:
    st.sidebar.info("Image not found for selected breed.")

# Sidebar - Attribute Filters
st.sidebar.subheader("Attribute Filters")

# Initialize attribute filters
attribute_filters = {}
for attribute in attribute_names:
    min_val, max_val = attribute_ranges[attribute]
    attribute_filters[attribute] = st.sidebar.slider(attribute, min_val, max_val, [min_val, max_val])

# Apply filters and get the filtered breeds
filtered_breeds = filter_breeds(attributes, list(attribute_filters.values()))

# Main page - Spyder plot and enlarged image
st.title("Dog Breed Selection System")

# Display the spyder plot
st.subheader("Dog Breed Attributes")
fig, ax = plt.subplots()
for breed in filtered_breeds.index:
    breed_attributes = attributes.loc[breed]
    breed_attributes = breed_attributes.append(breed_attributes[:1])  # Complete the loop
    ax.plot(breed_attributes.values, marker='o', label=breed)
ax.set_xticks(range(len(attribute_names)))
ax.set_xticklabels(attribute_names)
ax.legend(loc='upper right')
st.pyplot(fig)

# Display the enlarged image of the selected breed
st.subheader("Selected Breed Image")
if os.path.exists(image_path):
    st.image(image_path, use_column_width=True)
else:
    st.info("Image not found for selected breed.")

# Separate page for attribute filtering
st.title("Dog Breed Attribute Filtering")

# Display a separate page with tabs for each attribute
for attribute in attribute_names:
    st.subheader(attribute)
    filtered_breeds = filter_breeds(attributes, [attribute_filters[attribute]])
    filtered_breeds_names = filtered_breeds.index
    st.write(filtered_breeds_names)

# Page for breed comparison
st.title("Breed Comparison")

# Display the stacked bar plot for the filtered breeds
st.subheader("Filtered Dog Breeds Comparison")
fig, ax = plt.subplots()
filtered_breed_attributes = attributes.loc[filtered_breeds_names]
filtered_breed_attributes.plot(kind='bar', stacked=True, ax=ax)
ax.set_xticklabels(filtered_breeds_names, rotation=45)
st.pyplot(fig)

# Display breed names and pictures above the graph
st.subheader("Filtered Dog Breeds")
for breed in filtered_breeds_names:
    breed_image_path = os.path.join(img_dir, breed + ".png")
    if os.path.exists(breed_image_path):
        st.image(breed_image_path, caption=breed, width=100)
    else:
        st.write(breed)













