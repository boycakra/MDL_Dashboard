import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from compare import main
from overresults import results
from markallteam import homepage1

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

def homepage():

    st.title('MDL DATA MARK')
    # Streamlit widgets for filtering
    competition_id = st.selectbox('Select Competition ID', df['Competition_id'].unique())
    match_id = st.selectbox('Select Match ID', df[df['Competition_id'] == competition_id]['Match_id'].unique())
    round_id = st.selectbox('Select Round', df[(df['Competition_id'] == competition_id) & (df['Match_id'] == match_id)]['Round'].unique())
    team = st.selectbox('Select Team', df[(df['Competition_id'] == competition_id) & (df['Match_id'] == match_id) & (df['Round'] == round_id)]['Team'].unique())


    # Streamlit widget for selecting metrics
    selected_metrics = st.multiselect('Select Metrics', [
        'Kill Mid-lane',
        'Death Exp-lane',
        'Death Jungler-line',
        'Kill Jungler-line',
        'Death Roamer-lane',
        'Kill Roamer-lane',
        'Death Mid-lane',
        'Kill Exp-lane',
        'Kill gold-lane',
        'Death gold-lane'
    ])


    # Streamlit widgets for figure size
    fig_width = st.slider('Figure Width', min_value=5, max_value=20, value=10)
    fig_height = st.slider('Figure Height', min_value=5, max_value=20, value=8)

    # Filter data based on selections
    filtered_df = df[(df['Competition_id'] == competition_id) & (df['Match_id'] == match_id) & (df['Team'] == team)  & (df['Round'] == round_id) & (df['Event'].isin(selected_metrics))]

    # Convert percentage coordinates to pixel values
    filtered_df['Coordinates x'] = filtered_df['Coordinates x'] * img_width / 100
    filtered_df['Coordinates y'] = filtered_df['Coordinates y'] * img_height / 100

    # First figure: All events for the selected team
    fig1, ax1 = plt.subplots(figsize=(fig_width, fig_height))
    ax1.imshow(map_img, extent=[0, img_width, img_height, 0])
    sns.scatterplot(data=filtered_df, x='Coordinates x', y='Coordinates y', hue='Event', ax=ax1, s=100, legend='brief')
    ax1.set_title(f'Events Map for Team: {team}')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
    st.pyplot(fig1)


    # Additional widgets for Event-player and Event-Game
    event_player = st.selectbox('Select Event Player', ['Mid-lane', 'Jungler-line', 'Exp-lane', 'gold-lane', 'Roamer-lane'])
    event_game = st.selectbox('Select Event Game', ['Death', 'Kill'])

    # Filter data for the selected Event-player and Event-Game
    filtered_player_df = df[(df['Event-player'] == event_player) & (df['Event-Game'] == event_game) & (df['Round'] == round_id) & (df['Team'] == team)]

    # Convert percentage coordinates to pixel values
    filtered_player_df['Coordinates x'] = filtered_player_df['Coordinates x'] * img_width / 100
    filtered_player_df['Coordinates y'] = filtered_player_df['Coordinates y'] * img_height / 100

    
    # Second figure: Specific events for the selected player role and event game
    fig2, ax2 = plt.subplots(figsize=(fig_width, fig_height))
    ax2.imshow(map_img, extent=[0, img_width, img_height, 0])
    sns.scatterplot(data=filtered_player_df, x='Coordinates x', y='Coordinates y', hue='Event-Game', ax=ax2, s=100, legend='brief')
    ax2.set_title(f'{event_player} - {event_game} Events Map {team}')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
    st.pyplot(fig2)


# Add the imported function to the pages dictionary
pages = {
    "Homepage": homepage,
    "Team Map": homepage1,
    "Player Map": main,
    "Resulst Player": results 
    # Add the new page here
}

# Sidebar navigation (unchanged)
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Run the selected page function
pages[selection]()