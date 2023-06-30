import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px

origin_path = r"D:/Users/yaniv/OneDrive - post.bgu.ac.il/studies/university/Information Visualization/project/Project Code/"
origin_path = ""

st.set_page_config(page_title="Filter and Compare")
if not st.session_state:
    st.session_state['Friendliness'] = (1, 5)
    st.session_state['Energy'] = (1, 5)
    st.session_state['Protectiveness'] = (1, 5)
    st.session_state["Life Expectancy"] = (1, 5)
    st.session_state['Size'] = (1, 5)
    st.session_state['Maintenance'] = (1, 5)
attributes_components = {"Friendliness": ["Good with children", "Good with other dogs", "Good with strangers"],
                         "Energy": ["Energy", "Playfulness"],
                         "Protectiveness": ["Protective"],
                         "Life Expectancy": ["Life Expectancy"],
                         "Maintenance": ["Trainability", "Shedding", "Grooming", "Drooling", "Barking"],
                         "Size": ["Height"]}


def stacked_bar_plot(df):
    attributes = list(df.columns)
    attributes.remove("Name")

    # Calculate the total height of each bar
    df['Total'] = df[attributes].sum(axis=1)

    # Sort the DataFrame by the total height in descending order
    df_sorted = df.sort_values('Total', ascending=False)
    # define color palette for the bar plot
    palette = {'Maintenance': px.colors.qualitative.Plotly[4],
               'Size': px.colors.qualitative.G10[5],
               'Life Expectancy': px.colors.qualitative.Plotly[6],
               'Protectiveness': px.colors.qualitative.Plotly[9],
               'Energy': px.colors.qualitative.Plotly[2],
               'Friendliness': px.colors.qualitative.Plotly[3],
               }
    # Create a stacked bar plot with sorted data
    fig = go.Figure()

    for attribute in attributes:
        fig.add_trace(go.Bar(
            x=df_sorted["Name"],
            y=df_sorted[attribute],
            marker_color=palette[attribute],
            name=attribute,
            hovertemplate='<b>%{x}</b><br>' +
                          '%{text}<br>' +
                          'Total: %{customdata}' +
                          '<extra></extra>'
            ,
            customdata=df_sorted["Total"].apply(round, args=(3,)),
            text=[f'{attribute}: {round(y, 3)}' for y in df_sorted[attribute]],
            textposition='auto',
            textfont=dict(color='rgba(0, 0, 0, 0)')  # Make text transparent
        ))

    fig.update_layout(
        barmode='stack',
        yaxis=dict(range=[0, 30]),
        title="Comparison of Dog Breeds by Attributes",
        xaxis_title="Dog Breeds",
        yaxis_title="Attribute Score",
        legend_title="Attributes"
    )

    return fig

def lollipop_plot(df, attribute: str):
    ordered_df = df.sort_values(by=attribute)
    fig = go.Figure(go.Bar(
        x=ordered_df[attribute].values,
        y=ordered_df['Name'],
        orientation='h',
        width=0.01,
        marker_color="#60b4ff",
        hoverinfo="skip"))
    fig.add_scatter(x=ordered_df[attribute].apply(round, args=(3,)).values,
                    y=ordered_df['Name'],
                    mode='markers',
                    marker=dict(size=10),
                    marker_color="#ff4b4b",
                    hovertemplate='<b>%{y}</b><br>' +
                                  attribute + ': %{x}<br>' +
                                  '<extra></extra>'
                    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(211, 211, 211, 0.5)', tickvals=[1, 2, 3, 4, 5],
                     linecolor='black', linewidth=1, mirror=True)
    fig.update_yaxes(linecolor='black', linewidth=1, mirror=True)
    fig.update_layout(
        height=200 + 40 * (len(ordered_df) - 1),
        # width=1000,
        # height=5000,
        xaxis=dict(linecolor='white', linewidth=1, title_font=dict(size=14)),
        yaxis=dict(linecolor='white', linewidth=1, title_font=dict(size=14), tickfont=dict(size=14)),
        plot_bgcolor='black',
        xaxis_title=f'{attribute} Rating',
        yaxis_title='Breed Names',
        xaxis_range=[0, 5.1],
        showlegend=False
    )
    return fig


# Step 2 and 3: Filter dog breeds and display stacked bar plot
def filter_and_compare(df):
    st.markdown("# Step 2: Filter Dog Breeds")
    filtered_df = df.copy()
    # Display attribute tabs with selectbox for choosing lollipop plots
    attribute_names = list(df.columns)
    attribute_names.remove("Name")
    "Current Filters:"
    filters = st.container()
    filters_str = ""
    reset = st.button("Reset")
    if reset:
        st.session_state['Friendliness'] = (1, 5)
        st.session_state['Energy'] = (1, 5)
        st.session_state['Protectiveness'] = (1, 5)
        st.session_state["Life Expectancy"] = (1, 5)
        st.session_state['Size'] = (1, 5)
        st.session_state['Maintenance'] = (1, 5)
    st.markdown("")

    # for attribute in attribute_names:
    #     f"{attribute}: {list(st.session_state[attribute])}"
    left, right = st.columns(2)
    selected_attribute = right.selectbox("Select Attribute:", attribute_names)
    # st.markdown(f"# {selected_attribute}")
    min_val, max_val = left.slider("Choose your preference on a scale of 1 to 5:", key=selected_attribute, min_value=1,
                                   max_value=5,
                                   value=st.session_state[selected_attribute])
    del st.session_state[selected_attribute]
    st.session_state[selected_attribute] = (min_val, max_val)
    for attribute in attribute_names:
        min_val, max_val = st.session_state[attribute]
        filtered_df = filtered_df[
            (filtered_df[attribute] >= min_val) & (filtered_df[attribute] <= max_val)]

    for attribute in attribute_names:
        min_val, max_val = st.session_state[attribute]
        if st.session_state[attribute] == (1, 5):
            filters_str += f":blue[{attribute}: {min_val} - {max_val}] | "
        else:
            filters_str += f":red[{attribute}: {min_val} - {max_val}] | "
    filters.markdown(filters_str[:-2])
    st.markdown(f"""**{selected_attribute}** is composed of: {str(attributes_components[selected_attribute])[1:-1]}""")
    # Plot lollipop graph using the selected attribute data from `df`
    fig = lollipop_plot(filtered_df, selected_attribute)
    if not fig:
        st.markdown("# No dog is good enough for you:cry:")
        return
    # cols = st.columns([2,3,2])
    # st.pyplot(fig)
    st.plotly_chart(fig)
    # cols[1].pyplot(fig)

    # Compare button
    st.markdown("---")
    compare_button = st.button("Compare!", use_container_width=True, type="primary")

    # Perform comparison and display stacked bar plot
    if compare_button:
        st.markdown("# Step 3: Compare Dog Breeds")
        # Display stacked bar plot using the filtered dataframe
        fig = stacked_bar_plot(filtered_df)
        st.plotly_chart(fig)
        f"Dog images for reference:"
        dogs_per_row = 3
        columns_num_def = []
        total_dogs = len(filtered_df)
        while total_dogs - dogs_per_row > 0:
            columns_num_def.append(dogs_per_row)
            total_dogs -= dogs_per_row
        _ = columns_num_def.append(total_dogs) if total_dogs > 0 else None
        dog_idx = 0
        filtered_df = filtered_df.sort_values("Total", ascending=False)
        for i in range(len(columns_num_def)):
            if columns_num_def[i] == 1:
                dog = filtered_df.iloc[dog_idx]["Name"]
                image_path = origin_path + fr"dog_pics/{dog}.png"
                st.columns([1, 1, 1])[1].image(image_path, caption=dog, use_column_width=True)
                dog_idx += 1
            elif columns_num_def[i] == 2:
                cols = st.columns([1, 3, 1, 3, 1])
                dog = filtered_df.iloc[dog_idx]["Name"]
                image_path = origin_path + fr"dog_pics/{dog}.png"
                cols[1].image(image_path, caption=dog, use_column_width=True)
                dog_idx += 1
                dog = filtered_df.iloc[dog_idx]["Name"]
                image_path = origin_path + fr"dog_pics/{dog}.png"
                cols[3].image(image_path, caption=dog, use_column_width=True)
            else:
                cols = st.columns(columns_num_def[i])
                for col in cols:
                    dog = filtered_df.iloc[dog_idx]["Name"]
                    image_path = origin_path + fr"dog_pics/{dog}.png"
                    col.image(image_path, caption=dog, use_column_width=True)
                    dog_idx += 1


attributes = pd.read_csv(origin_path + r"norm_dog_attributes.csv")
filter_and_compare(attributes)
