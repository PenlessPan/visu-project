import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

print(st.session_state)
if not st.session_state:
    st.session_state['Friendliness'] = (1, 5)
    st.session_state['Energy'] = (1, 5)
    st.session_state['Protectiveness'] = (1, 5)
    st.session_state["Life Expectancy"] = (1, 5)
    st.session_state['Size'] = (1, 5)
    st.session_state['Maintenance'] = (1, 5)

def stacked_bar_plot(df):
    attributes = list(df.columns)
    attributes.remove("Name")

    # Calculate the total height of each bar
    df['Total'] = df[attributes].sum(axis=1)

    # Sort the DataFrame by the total height in descending order
    df_sorted = df.sort_values('Total', ascending=False)

    # Create a stacked bar plot with sorted data
    fig = go.Figure()

    for attribute in attributes:
        fig.add_trace(go.Bar(
            x=df_sorted["Name"],
            y=df_sorted[attribute],
            name=attribute
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
    my_range = range(1, len(df.index) + 1)

    # The horizontal plot is made using the hline function
    fig, ax = plt.subplots(figsize=(8, len(ordered_df)*0.3), nrows=1, ncols=1)
    plt.hlines(y=my_range, xmin=0, xmax=ordered_df[attribute], color='skyblue')
    plt.plot(ordered_df[attribute], my_range, "o")
    plt.xlim(0, 5.1)
    plt.yticks(my_range, ordered_df['Name'])
    plt.grid(True, axis="x")
    plt.title = "A vertical lolipop plot"
    plt.xlabel(f'{attribute} Score')
    plt.ylabel('Breed Names')
    return fig


# Step 2 and 3: Filter dog breeds and display stacked bar plot
def filter_and_compare(df):
    st.markdown("# Step 2: Filter Dog Breeds")
    filtered_df = df.copy()
    # Display attribute tabs with selectbox for choosing lollipop plots
    attribute_names = list(df.columns)
    attribute_names.remove("Name")
    reset = st.button("Reset")
    if reset:
        st.session_state['Friendliness'] = (1, 5)
        st.session_state['Energy'] = (1, 5)
        st.session_state['Protectiveness'] = (1, 5)
        st.session_state["Life Expectancy"] = (1, 5)
        st.session_state['Size'] = (1, 5)
        st.session_state['Maintenance'] = (1, 5)
    selected_attribute = st.selectbox("Select Attribute:", attribute_names)
    st.markdown(f"## {selected_attribute}")
    min_val, max_val = st.slider("Select min-max threshold:", key=selected_attribute, min_value=1, max_value=5,
                                 value=st.session_state[selected_attribute])
    del st.session_state[selected_attribute]
    st.session_state[selected_attribute] = (min_val, max_val)
    for attribute in attribute_names:
        f"{attribute} filters: {list(st.session_state[attribute])}"
    for attribute in attribute_names:
        min_val, max_val = st.session_state[attribute]
        filtered_df = filtered_df[
            (filtered_df[attribute] >= min_val) & (filtered_df[attribute] <= max_val)]

    # Plot lollipop graph using the selected attribute data from `df`
    fig = lollipop_plot(filtered_df, selected_attribute)
    # cols = st.columns([2,3,2])
    st.pyplot(fig)
    # cols[1].pyplot(fig)

    # Compare button
    st.markdown("---")
    compare_button = st.button("Compare!")

    # Perform comparison and display stacked bar plot
    if compare_button:
        st.markdown("# Step 3: Compare Dog Breeds")
        # Display stacked bar plot using the filtered dataframe
        fig = stacked_bar_plot(filtered_df)
        st.plotly_chart(fig)

attributes = pd.read_csv(r"dog_attributes.csv")
filter_and_compare(attributes)