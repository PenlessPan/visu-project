import pandas as pd
import matplotlib.pyplot as plt
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
temp['height'] = ((df['max_height_male'] + df['min_height_male']) / 2 + (
            df['max_height_female'] + df['min_height_female']) / 2) / 2
temp['weight'] = ((df['max_weight_male'] + df['min_weight_male']) / 2 + (
            df['max_weight_female'] + df['min_weight_female']) / 2) / 2
temp['coat_length'] = df['coat_length']


def scaler(col):
    return (col - col.min()) / (col.max() - col.min())


temp['height'] = (scaler(temp['height']) * 4) + 1
temp['weight'] = (scaler(temp['weight']) * 4) + 1
temp['coat_length'] = (scaler(temp['coat_length']) * 4) + 1

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

# Prepare data for visualization
breed_names = df['Name'].tolist()
attribute_data = attributes

# Function to get the breed image path
def get_breed_image_path(breed_name):
    return os.path.join(img_dir, breed_name + ".png")

# Function to get the breed attributes
def get_breed_attributes(breed_name):
    return attribute_data.loc[df['Name'] == breed_name].squeeze()

# Main page - Dog breed table
st.title("Dog Breed Selection System")

# Display the dog breed table
table_rows = []
for breed_name in breed_names:
    breed_image_path = get_breed_image_path(breed_name)
    breed_attributes = get_breed_attributes(breed_name)
    table_rows.append((breed_name, breed_image_path, breed_attributes))

table_cols = st.columns(4)
for breed_name, breed_image_path, _ in table_rows:
    with table_cols[0]:
        if os.path.exists(breed_image_path):
            st.image(breed_image_path, caption=breed_name, width=100)
        else:
            st.write(breed_name)
    with table_cols[1]:
        st.write("")

# Enlarged picture and spider plot for the last clicked breed
selected_breed = st.selectbox("Select a breed", breed_names)

selected_breed_image_path = get_breed_image_path(selected_breed)
if os.path.exists(selected_breed_image_path):
    st.image(selected_breed_image_path, caption=selected_breed, width=200)
else:
    st.write(selected_breed)

selected_breed_attributes = get_breed_attributes(selected_breed)

# Spider plot
fig, ax = plt.subplots()
selected_breed_attributes = selected_breed_attributes.append(selected_breed_attributes[:1])  # Complete the loop
ax.plot(selected_breed_attributes.values, marker='o')
ax.fill(selected_breed_attributes.values, alpha=0.3)
ax.set_xticks(range(len(attribute_names)))
ax.set_xticklabels(attribute_names)
st.pyplot(fig)









