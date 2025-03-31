import streamlit as st
import requests
from PIL import Image
import os

# Define paths to flag and team logo directories
path_to_flags = "asset/path_to_flags"
path_to_team_logos = "asset/path_to_team_logos"

# Function to load images safely and resize them to a standard size
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
        st.markdown("<h1 class='title'>Driver and Constructor Standings </h1>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)  # Adds two new lines

    st.markdown("<h2 class='subtitle'>Drivers Standings</h2>", unsafe_allow_html=True)

    # Driver Standings Section
    driver_standings_url = 'http://ergast.com/api/f1/current/driverStandings.json'
    response = requests.get(driver_standings_url)
    if response.status_code == 200:
        driver_standings = response.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

        # Display columns for headers
        header_cols = st.columns([2, 1, 5, 2, 1])  

        # Set headers in each column
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

        # Display driver standings with images and text layout
        for driver in driver_standings:
            driver_name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
            nationality = driver['Driver']['nationality']
            rank = driver["position"]
            points = driver["points"]
            wins = driver.get("wins", 0)

            # Load nationality flag
            flag_file = os.path.join(path_to_flags, f"{nationality}.png")
            flag_image = load_image(flag_file)

            # Display each row with flag image and details
            cols = st.columns([2, 1, 5, 2, 1]) 
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

    else:
        st.write("Error fetching driver standings")

    # Constructor Standings Section
    st.markdown("<h2 class='subtitle'>Constructor Standings</h2>", unsafe_allow_html=True)

    constructor_standings_url = 'http://ergast.com/api/f1/current/constructorStandings.json'
    response = requests.get(constructor_standings_url)
    if response.status_code == 200:
        constructor_standings = response.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]

        header_cols = st.columns([2, 1, 5, 2, 1])  

        # Set headers in each column
        with header_cols[0]:
            st.markdown("<div class='header'>Rank</div>", unsafe_allow_html=True)
        with header_cols[1]:
            st.markdown("<div class='header'>Logo</div>", unsafe_allow_html=True)
        with header_cols[2]:
            st.markdown("<div class='header'>Name</div>", unsafe_allow_html=True)
        with header_cols[3]:
            st.markdown("<div class='header'>Points</div>", unsafe_allow_html=True)
        with header_cols[4]:
            st.markdown("<div class='header'>Wins</div>", unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)  # Horizontal line divider

        # Display constructor standings with images and text layout
        for constructor in constructor_standings:
            team_name = constructor["Constructor"]["name"]
            rank = constructor["position"]
            points = constructor["points"]
            wins = constructor.get("wins", 0)

            # Load team logo
            logo_file = os.path.join(path_to_team_logos, f"{team_name.replace(' ', '_').lower()}.png")
            team_logo = load_team_image(logo_file)

            # Display each row with logo image and details
            cols = st.columns([2, 1, 5, 2, 1])  
            with cols[0]:
                st.markdown(f"<div class='ranking'>{rank}</div>", unsafe_allow_html=True)
            with cols[1]:
                if team_logo:
                    st.image(team_logo)
            with cols[2]:
                st.markdown(f"<div class='name'>{team_name}</div>", unsafe_allow_html=True)
            with cols[3]:
                st.markdown(f"<div class='points'>{points}</div>", unsafe_allow_html=True)
            with cols[4]:
                st.markdown(f"<div class='wins'>{wins}</div>", unsafe_allow_html=True)
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)  # Divider between entries

# Run the function if this script is executed directly
if __name__ == "__main__":
    ViewStanding()
