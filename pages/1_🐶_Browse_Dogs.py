import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.transforms import Affine2D
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.projections import register_projection
import numpy as np


st.set_page_config(page_title="Meet Our Dogs!", layout="wide")
origin_path = ""

df = pd.read_csv(origin_path + "norm_dog_attributes.csv")

# Function to create spider plots
def radar_factory(num_vars, frame='polygon'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def plot_spider(df, selected_breed):
    # Spider plot
    theta = radar_factory(6)
    data = list(df.loc[df['Name'] == selected_breed].drop(['Name'], axis=1).iloc[0])
    vals = df.drop(['Name'], axis=1)
    attribute_names = list(vals.columns)
    fig, ax = plt.subplots(figsize=(3, 3), nrows=1, ncols=1,
                           subplot_kw=dict(projection='radar'))
    ax.plot(theta, data)
    ax.fill(theta, data, alpha=0.45)
    ax.set_varlabels(attribute_names)
    ax.tick_params(axis='x', which='major', pad=9, labelsize=9, grid_color="black", grid_alpha=0.3)
    ax.tick_params(axis='y', pad=5, labelsize=8.3, direction='in', grid_color="black", grid_alpha=0.3)
    ax.set_rmax(5)
    ax.set_rgrids([1, 2, 3, 4, 5])
    ax.set_rlabel_position(0)
    ax.set_title(selected_breed)
    return fig


# Display table with dog breed images and names
def display_dog_table(df):
    st.markdown("# Meet Our Dogs!")
    st.markdown("Here you can browse through our dog breeds and look at the properties of breeds that peak your interest!\n\n Please take note that after selecting a breed you need to scroll to the bottom of the page in order to see the details.")
    num_columns = 10
    num_rows = len(df) // num_columns + 1
    def show_stats(breed_selected):
        st.sidebar.info("Please scroll down to look at the details!")
        text_col.markdown("# Breed Details")
        cols = breed_details_container.columns([1, 3, 2.5, 1])
        plot_col = cols[1]
        img_col = cols[2]
        image_path = origin_path + fr"dog_pics/{breed_selected}.png"
        img_col.image(image_path, caption=breed_selected, use_column_width=True)
        fig = plot_spider(df, breed_selected)
        plot_col.pyplot(fig)

    table_container = st.container()
    # Display the table with dog breed images and names
    with table_container:
        for row in range(num_rows):
            breed_row = df[row * num_columns: (row + 1) * num_columns]["Name"]
            breed_columns = st.columns(num_columns)
            for breed, column in zip(breed_row, breed_columns):
                image_path = origin_path + fr"dog_pics/{breed}.png"
                column.image(image_path, use_column_width=True)
                column.button(breed, on_click=show_stats, args=(breed,), use_container_width=True)
    breed_details_container = st.container()
    breed_details_container.markdown("---")
    text_col = breed_details_container.columns([2,1,2])[1]

display_dog_table(df)

