import streamlit as st
import pandas as pd
from PIL import Image
import os
from io import BytesIO
import base64
from dataBank import world_driver_championship_df 


seasons_file = 'data/seasons.csv'
races_file = 'data/races.csv'
results_file = 'data/results.csv'
driver_standings_file = 'data/driver_standings.csv'
drivers_file = 'data/drivers.csv'

def load_image(file_path):
    try:
        img = Image.open(file_path)
        return img  # Return the original image without resizing
    except FileNotFoundError:
        return None

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

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


def driver_info():
    
    # Header
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

    # display F1 logo and "Current Standing" beside it
    logo_file = os.path.join("asset/f1_red.png")
    team_logo = load_F1_image(logo_file)
    
    cols = st.columns([1, 5])
    with cols[0]:
        st.image(team_logo, width=175)
    with cols[1]:
        
        st.markdown("<h1 class='title' style='color: red; 'text-align: left; '>F1 Driver Profile</h1>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)  

    
    
    # load available years
    seasons_data = pd.read_csv(seasons_file)
    years = seasons_data['year'].unique()

    # dropdown for year selection
    selected_year = st.selectbox("Select Year", options=sorted(years, reverse=True))

    # filter data based on selected year
    races_data = pd.read_csv(races_file)
    selected_races = races_data[races_data['year'] == selected_year]

    results_data = pd.read_csv(results_file)
    race_ids = selected_races['raceId']
    selected_results = results_data[results_data['raceId'].isin(race_ids)]

    #get last race ID
    last_race_id = selected_races.loc[selected_races['round'].idxmax(), 'raceId']

    driver_standings_data = pd.read_csv(driver_standings_file)
    selected_driver_standings = driver_standings_data[driver_standings_data['raceId'] == last_race_id]
    world_championship_df = world_driver_championship_df()


    drivers_data = pd.read_csv(drivers_file)
    selected_drivers = drivers_data[drivers_data['driverId'].isin(selected_driver_standings['driverId'])]

    # add a dropdown for selecting drivers
    driver_names = ["ALL"] + [
        f"{driver['forename']} {driver['surname']}" for _, driver in selected_drivers.iterrows()
    ]
    selected_driver_name = st.selectbox("Select Driver", options=driver_names)

    # filter driver profiles based on selection
    if selected_driver_name == "ALL":
        drivers_to_display = selected_drivers
    else:
        drivers_to_display = selected_drivers[
            (selected_drivers['forename'] + " " + selected_drivers['surname']) == selected_driver_name
        ]

    # generate driver statistics for filtered drivers
    driver_info_list = []
    for _, driver in drivers_to_display.iterrows():
        driver_id = driver['driverId']
        driver_name = f"{driver['forename']} {driver['surname']}"
        driver_code = driver.get('code', 'N/A')
        driver_number = driver.get('number', 'N/A')
        dob = driver['dob']
        nationality = driver['nationality']
        url = driver['url']
        
        # career stats
        driver_results = results_data[results_data['driverId'] == driver_id]
        podiums = driver_results[driver_results['positionText'].isin(['1', '2', '3'])].shape[0]
        wins = driver_results[driver_results['positionText'] == '1'].shape[0]
        races_started = driver_results[driver_results['positionText'].str.isdigit() | (driver_results['positionText'] == 'R')].shape[0]
        races_finished = driver_results[driver_results['positionText'].str.isdigit()].shape[0]
        retired = driver_results[driver_results['positionText'] == 'R'].shape[0]
        disqualified = driver_results[driver_results['positionText'] == 'D'].shape[0]
        career_points = round(driver_results['points'].sum(), 2)
        world_championships = world_championship_df[world_championship_df['Driver ID'] == driver_id].shape[0]
        poles = driver_results[driver_results['grid'] == 1].shape[0]

        # create driver statistics
        driver_info = {
            'Driver Name': driver_name,
            'Driver Code': driver_code,
            'Driver Number': driver_number,
            'Date of Birth': dob,
            'Nationality': nationality,
            'Career Points': career_points,
            'World Championships': world_championships,
            'Poles': poles,
            'Podiums': podiums,
            'Wins': wins,
            'Races Started': races_started,
            'Races Finished': races_finished,
            'Retired': retired,
            'Disqualified': disqualified,
            'More Information': url
        }
        driver_info_list.append(driver_info)

    # driver statistics in containers
    for driver in driver_info_list:
        with st.container():
            st.markdown(
                f"""
                <div style="text-align: center; margin-left: -50px; font-size: 24px;  font-weight: bold; color: {'#E30613'};">
                    {driver['Driver Name']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # image at the top, spanning the entire width
            image_path = f"asset/path_to_driver/{driver['Driver Code']}.png"
            image = load_image(image_path)
            if image:
                image_base64 = image_to_base64(image)
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-left: -50px;">
                        <img src="data:image/png;base64,{image_base64}" width="400"/>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # create two columns below the image
            cols = st.columns(2)  # two equally sized columns

            # Column 1: Basic Info
            with cols[0]:
                st.write(f"**Driver Code:** {driver['Driver Code']}")
                st.write(f"**Driver Number:** {driver['Driver Number']}")
                st.write(f"**Date of Birth:** {driver['Date of Birth']}")
                st.write(f"**Nationality:** {driver['Nationality']}")
                st.write(f"**World Championships:** {driver['World Championships']}")
                st.write(f"**Wins:** {driver['Wins']}")
                st.write(f"**Career Points:** {driver['Career Points']}")

            # Column 2: Remaining Stats
            with cols[1]:
                st.write(f"**Poles:** {driver['Poles']}")
                st.write(f"**Podiums:** {driver['Podiums']}")
                st.write(f"**Races Started:** {driver['Races Started']}")
                st.write(f"**Races Finished:** {driver['Races Finished']}")
                st.write(f"**Retired:** {driver['Retired']}")
                st.write(f"**Disqualified:** {driver['Disqualified']}")
                st.markdown(f"[More Information]({driver['More Information']})")
            st.markdown(
                f"""
                <hr style="border: 2px solid {'#E30613'}; margin: 30px 0;"/>
                """,
                unsafe_allow_html=True,
            )

if __name__ == "__main__":
    driver_info()


