import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Load data
data_path = 'eventsmap.csv'
df = pd.read_csv(data_path)

# Function to clean and convert coordinate strings to float
def clean_coordinate(coord):
    return float(re.sub(r'[()%]', '', coord))

# Apply cleaning function to the coordinate columns
df['Coordinates x'] = df['Coordinates x'].apply(clean_coordinate)
df['Coordinates y'] = df['Coordinates y'].apply(clean_coordinate)

# Set the background image for the plot
map_image_path = 'map.PNG'
map_img = plt.imread(map_image_path)
img_height, img_width = map_img.shape[:2]

def main():
    # Streamlit widgets for filtering
    competition_id = st.selectbox('Select Competition ID', df['Competition_id'].unique())
    match_id = st.selectbox('Select Match ID', df[df['Competition_id'] == competition_id]['Match_id'].unique())
    round_id = st.selectbox('Select Round', df[(df['Competition_id'] == competition_id) & (df['Match_id'] == match_id)]['Round'].unique())

    # Determine the teams playing in the specified competition, match, and round
    teams_playing = df[(df['Competition_id'] == competition_id) & (df['Match_id'] == match_id) & (df['Round'] == round_id)]['Team'].unique()
    if len(teams_playing) != 2:
        st.error('There should be exactly two teams playing in the specified competition, match, and round.')
        st.stop()

    team_a, team_b = teams_playing

    # Additional widgets for Event-player
    event_player_team_a = st.selectbox(f'Select Event Player for {team_a}', ['Mid-lane', 'Jungler-line', 'Exp-lane', 'Gold-lane', 'Roamer-lane'])
    event_player_team_b = st.selectbox(f'Select Event Player for {team_b}', ['Mid-lane', 'Jungler-line', 'Exp-lane', 'Gold-lane', 'Roamer-lane'])

    # Checkboxes for Event Game
    event_game_death = st.checkbox('Death', value=True)
    event_game_kill = st.checkbox('Kill', value=True)

    selected_event_games = []
    if event_game_death:
        selected_event_games.append('Death')
    if event_game_kill:
        selected_event_games.append('Kill')

    # Filter data for the selected competition, match, round, and event games
    filtered_df = df[(df['Competition_id'] == competition_id) & (df['Match_id'] == match_id) & (df['Round'] == round_id) & (df['Event-Game'].isin(selected_event_games))]

    # Separate data for the two teams based on the selected event players
    team_a_df = filtered_df[(filtered_df['Event-player'] == event_player_team_a) & (filtered_df['Team'] == team_a)]
    team_b_df = filtered_df[(filtered_df['Event-player'] == event_player_team_b) & (filtered_df['Team'] == team_b)]

    # Convert percentage coordinates to pixel values for Team A
    team_a_df['Coordinates x'] = team_a_df['Coordinates x'] * img_width / 100
    team_a_df['Coordinates y'] = team_a_df['Coordinates y'] * img_height / 100

    # Convert percentage coordinates to pixel values for Team B
    team_b_df['Coordinates x'] = team_b_df['Coordinates x'] * img_width / 100
    team_b_df['Coordinates y'] = team_b_df['Coordinates y'] * img_height / 100

    # Combine data for plotting
    plot_df = pd.concat([team_a_df, team_b_df])

    # Plot the scatter plot
    fig4, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(map_img, extent=[0, img_width, img_height, 0])

    # Plot data
    sns.scatterplot(
        data=plot_df, 
        x='Coordinates x', 
        y='Coordinates y', 
        hue='Team', 
        style='Event-Game', 
        markers={'Death': 'X', 'Kill': 'o'}, 
        ax=ax, 
        s=100
    )

    ax.set_title(f'Events Map: {event_player_team_a} ({team_a}) vs {event_player_team_b} ({team_b})')

    # Place legend outside the plot
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig4)

if __name__ == "__main__":
    main()
