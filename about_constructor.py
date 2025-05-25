import streamlit as st
import pandas as pd
from PIL import Image
import os
from io import BytesIO
import base64
from dataBank import world_constructors_championship_df 


# Paths to data files
seasons_file = 'data/seasons.csv'
races_file = 'data/races.csv'
results_file = 'data/results.csv'
constructors_standings_file = 'data/constructor_standings.csv'
constructors_file = 'data/constructors.csv'

def load_image(file_path):
    try:
        img = Image.open(file_path)
        return img 
    except FileNotFoundError:
        return None

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def load_F1_image(file_path, size=(400, 155)):
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

def constructors_info():
    
    # Header
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
        st.markdown("<br>", unsafe_allow_html=True)  # Adds two new lines
        st.image(team_logo, width=175)
    with cols[1]:
        st.markdown(
            "<h1 class='title' style='color: red; text-align: center; margin-bottom: 0;'>F1 Constructors Profile</h1>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)  # Adds two new lines

    

    seasons_data = pd.read_csv(seasons_file)
    years = seasons_data['year'].unique()

    # Dropdown for year selection
    selected_year = st.selectbox("Select Year", options=sorted(years, reverse=True))
    races_data = pd.read_csv(races_file)
    selected_races = races_data[races_data['year'] == selected_year]

    results_data = pd.read_csv(results_file)
    race_ids = selected_races['raceId']
    selected_results = results_data[results_data['raceId'].isin(race_ids)]

    # Get last race ID
    last_race_id = selected_races.loc[selected_races['round'].idxmax(), 'raceId']
    constructors_standings_data = pd.read_csv(constructors_standings_file)
    selected_constructors_standings = constructors_standings_data[constructors_standings_data['raceId'] == last_race_id]

    world_championship_df = world_constructors_championship_df()
    
    constructors_data = pd.read_csv(constructors_file)
    selected_constructors = constructors_data[constructors_data['constructorId'].isin(selected_constructors_standings['constructorId'])]
    
    # Add constructor selection
    constructor_options = ["All"] + list(selected_constructors['name'])
    selected_constructor = st.selectbox("Select Constructor", options=constructor_options)

    # Filter constructors based on selection
    if selected_constructor != "All":
        selected_constructors = selected_constructors[selected_constructors['name'] == selected_constructor]

    # Generate Constructor statistics
    constructors_info_list = []
    for _, constructor in selected_constructors.iterrows():
        constructor_id = constructor['constructorId']
        constructor_name = f"{constructor['name']}"
        constructor_code = constructor.get('constructorRef', 'N/A')
        nationality = constructor['nationality']
        url = constructor['url']

        # Career stats
        constructor_results = results_data[results_data['constructorId'] == constructor_id]
        podiums = constructor_results[constructor_results['positionText'].isin(['1', '2', '3'])].shape[0]
        wins = constructor_results[constructor_results['positionText'] == '1'].shape[0]
        races_started = constructor_results[constructor_results['positionText'].str.isdigit() | (constructor_results['positionText'] == 'R')].shape[0]
        races_finished = constructor_results[constructor_results['positionText'].str.isdigit()].shape[0]
        retired = constructor_results[constructor_results['positionText'] == 'R'].shape[0]
        disqualified = constructor_results[constructor_results['positionText'] == 'D'].shape[0]
        career_points = round(constructor_results['points'].sum(), 2)
        world_championships = world_championship_df[world_championship_df['Constructor ID'] == constructor_id].shape[0]
        poles = constructor_results[constructor_results['grid'] == 1].shape[0]

        # Create Constructor statistics
        constructor_info = {
            'Constructor Name': constructor_name,
            'Nationality': nationality,
            'Constructor Points': career_points,
            'Constructor Code': constructor_code,
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
        constructors_info_list.append(constructor_info)

    # Display Constructor statistics
    for constructor in constructors_info_list:
        with st.container():
            st.markdown(
                f"""
                <div style="text-align: center; margin-left: -50px; font-size: 24px;  font-weight: bold; color: {'#E30613'};">
                    {constructor['Constructor Name']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Display the image at the top, spanning the entire width
            image_path = f"asset/path_to_constructor/{constructor['Constructor Code']}.png"
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

            # Create two columns below the image
            cols = st.columns(2)  # Two equally sized columns

            # Column 1: Basic Info
            with cols[0]:
                st.write(f"**Nationality:** {constructor['Nationality']}")
                st.write(f"**World Championships:** {constructor['World Championships']}")
                st.write(f"**Wins:** {constructor['Wins']}")
                st.write(f"**Constructor Points:** {constructor['Constructor Points']}")
                st.write(f"**Poles:** {constructor['Poles']}")
                st.write(f"**Podiums:** {constructor['Podiums']}")

            # Column 2: Remaining Stats
            with cols[1]:
                st.write(f"**Races Started:** {constructor['Races Started']}")
                st.write(f"**Races Finished:** {constructor['Races Finished']}")
                st.write(f"**Retired:** {constructor['Retired']}")
                st.write(f"**Disqualified:** {constructor['Disqualified']}")
                st.markdown(f"[More Information]({constructor['More Information']})")

            st.markdown(
                f"""
                <hr style="border: 2px solid {'#E30613'}; margin: 30px 0;"/>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    constructors_info()


