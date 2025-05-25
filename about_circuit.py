import streamlit as st
import pandas as pd
from PIL import Image
import os
from io import BytesIO
import base64

# data files
seasons_file = 'data/seasons.csv'
races_file = 'data/races.csv'
results_file = 'data/results.csv'
constructors_standings_file = 'data/constructor_standings.csv'
constructors_file = 'data/constructors.csv'
circuits_file = 'data/circuits.csv'
drivers_file = 'data/drivers.csv'


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

def load_logo_image(file_path, size=(400, 155)):
    try:
        img = Image.open(file_path)
        img = img.resize(size)  
        return img
    except FileNotFoundError:
        return None
def load_F1_image(file_path):
    try:
        img = Image.open(file_path)
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

def circuit_info():

    st.markdown(
        """
        <style>
            .title {
                font-size: 34px;
                color: #FF1E00; /* F1 Red */
                text-align: center;
            }
            .header {
                font-size: 18px;
                font-weight: bold;
                color: #FF1E00; /* F1 Red */
                text-align: center;
                margin-top: 20px; /* Increase margin for spacing */
            }
            .divider {
                margin: 10px 0;
                border: 1px solid #FF1E00; /* F1 Red */
            }
            .details {
                text-align: center;
                font-size: 16px;
                color: #FFFFFF; /* White */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display F1 logo and title
    logo_file = os.path.join("asset/f1_red.png")
    team_logo = load_logo_image(logo_file)
    
    cols = st.columns([1, 5])
    with cols[0]:
        st.markdown("<br>", unsafe_allow_html=True)  # Adds two new lines
        st.image(team_logo, width=175)
    with cols[1]:
        
        st.markdown("<h1 class='title' style='color: red; 'text-align: left; '>F1 Circuits Profile</h1>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)  # Adds two new lines

    # load the seasons data
    seasons_data = pd.read_csv(seasons_file)
    years = seasons_data['year'].unique()
    # load the circuits data
    circuits_data = pd.read_csv(circuits_file)
    results_data = pd.read_csv(results_file)
    drivers_data = pd.read_csv(drivers_file)
    constructors_data = pd.read_csv(constructors_file)

    # dropdown for year selection
    selected_year = st.selectbox("Select Year", options=sorted(years, reverse=True))
    races_data = pd.read_csv(races_file)
    selected_races = races_data[races_data['year'] == selected_year]

    selected_circuits = selected_races['circuitId'].unique()
    matching_circuits = circuits_data[circuits_data['circuitId'].isin(selected_circuits)]
    circuit_names = ["All"] + matching_circuits['name'].values.tolist()
    
    selected_circuit_name = st.selectbox("Select Circuit", options=circuit_names)

    if selected_circuit_name == "All":
        circuit_ids_to_process = selected_circuits
    else:
        circuit_ids_to_process = matching_circuits[matching_circuits['name'] == selected_circuit_name]['circuitId'].values

    # display circuit details for each selected circuit
    for circuit_id in circuit_ids_to_process:
        
        # circuit details
        circuit_details = circuits_data[circuits_data['circuitId'] == circuit_id].iloc[0]
        circuit_name = circuit_details['name']
        location = circuit_details['location']
        country = circuit_details['country']
        url = circuit_details['url']
        circuit_ref = circuit_details['circuitRef']
        circuit_image = load_F1_image(f"asset/path_to_circuit/{circuit_ref}.png")

        # counr races per circuit
        count_races = len(races_data[races_data['circuitId'] == circuit_id])
        first_race = races_data[races_data['circuitId'] == circuit_id]['year'].min()

        # fastest Lap Record
        race_ids = races_data[races_data['circuitId'] == circuit_id]['raceId'].unique()
        circuit_races_data = results_data[results_data['raceId'].isin(race_ids)]
        fastest_lap_time = results_data[results_data['raceId'].isin(race_ids)]['fastestLapTime'].min()
        fastest_lap_row = results_data[(results_data['raceId'].isin(race_ids)) & (results_data['fastestLapTime'] == fastest_lap_time)]
        fastest_lap_speed = fastest_lap_row['fastestLapSpeed'].values[0]
        
        # number of Laps
        num_laps = results_data[results_data['raceId'].isin(race_ids)]['laps'].max()

        # lap Record Driver ID and Name
        lap_record_driver_id = fastest_lap_row['driverId'].values[0] 
        lap_record_driver_name = drivers_data[drivers_data['driverId'] == lap_record_driver_id]['forename'].values[0] + " " + drivers_data[drivers_data['driverId'] == lap_record_driver_id]['surname'].values[0]


        # most Wins Driver
        wins_data = circuit_races_data[circuit_races_data['positionText'] == "1"]
        most_wins_driver_id = wins_data['driverId'].value_counts().idxmax()
        most_wins_driver_name = drivers_data[drivers_data['driverId'] == most_wins_driver_id]['forename'].values[0] + " " + drivers_data[drivers_data['driverId'] == most_wins_driver_id]['surname'].values[0]
        
        # most Wins Constructor
        most_wins_constructor_id = wins_data['constructorId'].value_counts().idxmax()
        most_wins_constructor_name = constructors_data[constructors_data['constructorId'] == most_wins_constructor_id]['name'].values[0]

        # display information
        st.markdown(
                f"""
                <div style="text-align: center; margin-left: -50px; font-size: 24px;  font-weight: bold; color: {'#E30613'};">
                    {circuit_name}
                </div>
                """,
                unsafe_allow_html=True,
            )

        if circuit_image:
            st.image(circuit_image)
        left_col, right_col = st.columns(2)

        # left column details
        with left_col:
            st.write(f"**Location:** {location}")
            st.write(f"**Country:** {country}")
            st.write(f"**First Race:** {first_race}")
            st.write(f"**Total Races:** {count_races}")
            st.write(f"**Number of Laps:** {num_laps}")
            st.markdown(f"[More Information]({url})")

        # right column details
        with right_col:
            st.write(f"**Fastest Lap Time:** {fastest_lap_time}")
            st.write(f"**Fastest Lap Speed:** {fastest_lap_speed} km/h")
            st.write(f"**Lap Record Driver:** {lap_record_driver_name}")
            st.write(f"**Most Wins Driver:** {most_wins_driver_name}")
            st.write(f"**Most Wins Constructor:** {most_wins_constructor_name}")

if __name__ == "__main__":
    circuit_info()
