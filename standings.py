import streamlit as st
import pandas as pd
from PIL import Image
from dataBank import driversStandingsDf
import os

# Paths to data files
seasons_file = 'data/seasons.csv'
races_file = 'data/races.csv'
results_file = 'data/results.csv'
driver_standings_file = 'data/driver_standings.csv'
drivers_file = 'data/drivers.csv'

# Utility functions for loading images
def load_image(file_path, size=(45, 25)):
    try:
        img = Image.open(file_path)
        img = img.resize(size)  
        return img
    except FileNotFoundError:
        return None

def load_F1_image(file_path, size=(350, 155)):
    try:
        img = Image.open(file_path)
        img = img.resize(size)  
        return img
    except FileNotFoundError:
        return None

def load_team_image(file_path, size=(40, 40)):
    try:
        img = Image.open(file_path)
        img = img.resize(size)  
        return img
    except FileNotFoundError:
        return None

# Function to display driver standings
def display_driver_standings(selected_driver_standings, selected_drivers):
    selected_driver_standings = selected_driver_standings.merge(
        selected_drivers, on='driverId', how='inner'
    )
    selected_driver_standings['Driver Full Name'] = selected_driver_standings['forename'] + " " + selected_driver_standings['surname']
    selected_driver_standings = selected_driver_standings.sort_values(by='position')

    # Display standings with new header format
    st.markdown("<h2 class='subtitle'>Driver Standings</h2>", unsafe_allow_html=True)

    # Custom header layout
    header_cols = st.columns([2, 1, 5, 2, 1])  # Adjusted for a neat layout
    with header_cols[0]:
        st.markdown("<div class='header'>Rank</div>", unsafe_allow_html=True)
    with header_cols[1]:
        st.markdown("<div class='header'>Flag</div>", unsafe_allow_html=True)
    with header_cols[2]:
        st.markdown("<div class='header'>Name</div>", unsafe_allow_html=True)
    with header_cols[3]:
        st.markdown("<div class='header'>Points</div>", unsafe_allow_html=True)
    with header_cols[4]:
        st.markdown("<div class='header'>Wins</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)  # Horizontal line divider

    # Display driver standings with image and details
    for _, row in selected_driver_standings.iterrows():
        driver_name = row['Driver Full Name']
        nationality = row['nationality']
        rank = row['position']
        points = round(row['points'])  # Round points to nearest integer
        wins = row['wins']

        # Load nationality flag
        flag_file = os.path.join("asset/path_to_flags", f"{nationality}.png")
        flag_image = load_image(flag_file)

        # Display each row with flag image and details
        cols = st.columns([2, 1, 5, 2, 1])  # Adjusted for a neat layout
        with cols[0]:
            st.markdown(f"<div class='ranking'>{rank}</div>", unsafe_allow_html=True)
        with cols[1]:
            if flag_image:
                st.image(flag_image)
        with cols[2]:
            st.markdown(f"<div class='name'>{driver_name}</div>", unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f"<div class='points'>{points}</div>", unsafe_allow_html=True)
        with cols[4]:
            st.markdown(f"<div class='wins'>{wins}</div>", unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)  # Divider between entries

# Function to display constructor standings
def display_constructor_standings(selected_constructor_standings):
    st.markdown("<h2 class='subtitle'>Constructor Standings</h2>", unsafe_allow_html=True)
    # Constructor standings can be added similarly, using the same approach as driver standings.
    # Example placeholder for constructor standings implementation
    for _, row in selected_constructor_standings.iterrows():
        constructor_name = row['name']
        points = round(row['points'])  # Round points to nearest integer
        st.markdown(f"<div class='ranking'>{constructor_name} - Points: {points}</div>", unsafe_allow_html=True)

# Main function to display standings
def ViewStanding():
    # Set F1 theme styles
    st.markdown(
        """
        <style>
            .title {
                font-size: 34px;
                color: #FF1E00; /* F1 Red */
                text-align: center;
            }
            .subtitle {
                font-size: 30px;
                color: #FFFFFF; /* Black */
                text-align: center;
                margin-top: 20px;  /* Increase margin for spacing */
            }
            .header {
                font-size: 18px;
                font-weight: bold;
                color: #FF1E00; /* F1 Red */
                text-align: center;
                margin-top: 30px;  /* Increase margin for spacing */
            }
            .divider {
                margin: 10px 0;
                border: 1px solid #FF1E00; /* F1 Red */
            }
            .ranking, .points, .wins {
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display F1 logo and "Current Standing" beside it
    logo_file = os.path.join("asset/f1_red.png")
    team_logo = load_F1_image(logo_file)
    
    cols = st.columns([1, 5])
    with cols[0]:
        st.image(team_logo, width=130)
    with cols[1]:
        st.markdown("<h1 class='title'; style='color: red;'>Driver and Constructor Standings</h1>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)  # Adds two new lines

    # Load available years
    seasons_data = pd.read_csv(seasons_file)
    years = seasons_data['year'].unique()

    # Dropdown for year selection
    selected_year = st.selectbox("Select Year", options=sorted(years, reverse=True))

    # get the drivers data and display it
    selected_driver_standings, selected_drivers = driversStandingsDf(selected_year)
    display_driver_standings(selected_driver_standings, selected_drivers)

    # Constructor standings placeholder 


# Run the function if this script is executed directly
if __name__ == "__main__":
    ViewStanding()
