import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from matplotlib.patches import Patch
from math import pi

# Load data
data_path = 'eventsmap.csv'
df = pd.read_csv(data_path)

# Function to clean and convert coordinate strings to float
def clean_coordinate(coord):
    # Remove parentheses and percentage sign, then convert to float
    return float(re.sub(r'[()%]', '', coord))

# Apply cleaning function to the coordinate columns
df['Coordinates x'] = df['Coordinates x'].apply(clean_coordinate)
df['Coordinates y'] = df['Coordinates y'].apply(clean_coordinate)

# Set the background image for the plot
map_image_path = 'map.PNG'

# Load the background image and get its dimensions
map_img = plt.imread(map_image_path)
img_height, img_width = map_img.shape[:2]

def radar_chart(data, teams, fig_width=10, fig_height=8):
    # Create radar chart for multiple teams
    metrics = [
        'Kill Mid-lane',
        'Death Exp-lane',
        'Death Jungler-line',
        'Kill Jungler-line',
        'Death Roamer-lane',
        'Kill Roamer-lane',
        'Death Mid-lane',
        'Kill Exp-lane',
        'Kill Gold-lane',
        'Death Gold-lane'
    ]
    
    num_vars = len(metrics)
    
    # Compute angle for each metric
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), subplot_kw=dict(polar=True))
    
    for team in teams:
        values = data[data['Team'] == team][metrics].mean().tolist()
        values += values[:1]
        ax.plot(angles, values, label=team)
        ax.fill(angles, values, alpha=0.1)

    # Labels for each metric
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)

    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    
    return fig

def homepage1():
    st.title('MDL Team DATA MARK')
    # Streamlit widgets for filtering
    competition_id = st.selectbox('Select Competition ID', df['Competition_id'].unique())
    match_id = st.selectbox('Select Match ID', df[df['Competition_id'] == competition_id]['Match_id'].unique())
    round_id = st.selectbox('Select Round', df[(df['Competition_id'] == competition_id) & (df['Match_id'] == match_id)]['Round'].unique())
    teams = st.multiselect('Select Teams', df[(df['Competition_id'] == competition_id) & (df['Match_id'] == match_id) & (df['Round'] == round_id)]['Team'].unique())

    # Streamlit widgets for figure size
    fig_width = st.slider('Figure Width', min_value=5, max_value=20, value=10)
    fig_height = st.slider('Figure Height', min_value=5, max_value=20, value=8)

    # Filter data based on selections
    filtered_df = df[(df['Competition_id'] == competition_id) & (df['Match_id'] == match_id) & (df['Round'] == round_id) & (df['Team'].isin(teams))]

    # Convert percentage coordinates to pixel values
    filtered_df['Coordinates x'] = filtered_df['Coordinates x'] * img_width / 100
    filtered_df['Coordinates y'] = filtered_df['Coordinates y'] * img_height / 100

    # First figure: All events for the selected teams
    fig1, ax1 = plt.subplots(figsize=(fig_width, fig_height))
    ax1.imshow(map_img, extent=[0, img_width, img_height, 0])
    sns.scatterplot(data=filtered_df, x='Coordinates x', y='Coordinates y', hue='Event', ax=ax1, s=100, legend='brief')
    ax1.set_title(f'Events Map for Teams: {", ".join(teams)}')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
    st.pyplot(fig1)

if __name__ == "__main__":
    homepage1()
