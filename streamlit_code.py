import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


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
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

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
theta = radar_factory(6)
data = list(attributes.loc[attributes['Name'] == "Beagle"].drop(['Name'], axis=1).iloc[0])
vals = attributes.drop(['Name'], axis=1)
attribute_names = list(vals.columns)
fig, axs = plt.subplots(figsize=(3, 3), nrows=1, ncols=1,
                        subplot_kw=dict(projection='radar'))
axs.plot(theta, data)
axs.fill(theta, data, alpha=0.45)
axs.set_varlabels(attribute_names)
st.pyplot(fig)

