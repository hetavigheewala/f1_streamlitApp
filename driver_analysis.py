import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image


seasons_file = 'data/seasons.csv'
races_file = 'data/races.csv'
results_file = 'data/results.csv'
driver_standings_file = 'data/driver_standings.csv'
drivers_file = 'data/drivers.csv'
constructors_standings_file = 'data/constructor_standings.csv'
constructors_file = 'data/constructors.csv'

def load_F1_image(file_path, size=(400, 155)):
    try:
        img = Image.open(file_path)
        img = img.resize(size)  
        return img
    except FileNotFoundError:
        return None

def top_10_driver_by_points(driver_analysis_df, selected_year):
    # Load necessary data
    races_data = pd.read_csv(races_file)
    results_data = pd.read_csv(results_file)

    # Filter races based on the selected year
    if selected_year == "All":
        selected_races = races_data
    else:
        selected_races = races_data[races_data['year'] == int(selected_year)]
    
    race_ids = selected_races['raceId'].tolist()

    # Filter results to only include the selected races
    selected_results_data = results_data[results_data['raceId'].isin(race_ids)]

    # Get all unique driver IDs from the filtered results
    selected_drivers = selected_results_data['driverId'].unique()

    # Filter the driver analysis DataFrame to only include the selected drivers
    selected_drivers_analysis = driver_analysis_df[driver_analysis_df['driverId'].isin(selected_drivers)]

    # Sort the filtered drivers by career points in descending order
    top_drivers = selected_drivers_analysis.sort_values(by='Career Points', ascending=False).head(10)

    # Use Streamlit to display the results
    st.markdown(
        f"""
            <div style="text-align: center; margin-left: -50px; font-size: 30px;  font-weight: bold; color: {'#E30613'};">
            Top 10 Drivers by Career Points
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.write(
        """
            The Top 10 Drivers Career Points Analysis highlights the most consistent and successful drivers based on their total career points. It helps spot performance patterns and compare drivers across eras. Filtering by season shows who competed and excelled in specific years, giving insights into career evolution and dominance. The vertical bar chart displays the top 10 drivers’ career points, with each bar labeled by driver code and hover details showing full name and car number. This static comparison focuses on overall achievements, making it easy to explore F1’s competitive history and the legacy of its top talents.        """
    )
    
    color_scheme = [
        '#00D7B6', '#4781D7', '#ED1131', '#F47600', '#00A1E8',
        '#6C98FF', '#229971', '#1868DB', '#01C00E', '#9C9FA2'
    ]

    # Map the colors to the drivers
    top_drivers['Color'] = color_scheme[:len(top_drivers)]
    top_drivers['hover_text'] = top_drivers['number'] + " " + top_drivers['forename'] + " " + top_drivers['surname'].astype(str)

    chart_data = top_drivers[['code', 'Career Points']].set_index('code')

    # Streamlit bar chart
    st.bar_chart(chart_data)

    
def driver_analysis_page():

    # header with logo
    logo_file = os.path.join("asset/f1_red.png")
    team_logo = load_F1_image(logo_file)
    
    cols = st.columns([1, 5])
    with cols[0]:
        st.markdown("<br>", unsafe_allow_html=True)  # Adds two new lines
        st.image(team_logo, width=175)
    with cols[1]:
        st.markdown(
            "<h1 class='title' style='color: red; text-align: left; margin-bottom: 0;'>F1 Driver's Analysis</h1>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True) 
    
    seasons_data = pd.read_csv(seasons_file)
    years = ["All"] + list(seasons_data['year'].unique())
    selected_year = st.selectbox("Select Year", options=sorted(years, reverse=True, key=lambda x: str(x)))
    
    # create analysis database
    crash_status_ids = [3, 4, 104, 130]             # Crashes status IDs

    results_data = pd.read_csv(results_file)
    drivers_data = pd.read_csv(drivers_file)

    # empty list to store driver metrics
    driver_metrics = []

    # unique driver IDs
    unique_driver_ids = results_data['driverId'].unique()

    # iterate over each driver
    for driver_id in unique_driver_ids:
        # filter data for the current driver
        driver_data = results_data[results_data['driverId'] == driver_id]
        
        career_points = round(driver_data['points'].sum(), 2)                            # Career Points
        career_wins = (driver_data['positionOrder'] == 1).sum()                             # Career Wins
        career_poles = (driver_data['grid'] == 1).sum()                                     # Career Poles
        avg_position_finish = driver_data[driver_data['points'] != '/N']['points'].mean()   # Average Position Finish
        avg_qualifying = driver_data['grid'].mean()                                         # Average Qualifying
        total_races = driver_data['raceId'].nunique()                                       # Races
        
        # Races to First Race Win
        first_win_race_id = driver_data[driver_data['positionOrder'] == 1]['raceId'].min()
        races_to_first_win = driver_data[driver_data['raceId'] < first_win_race_id]['raceId'].count() if pd.notna(first_win_race_id) else None
        # Races from Last Race Win
        last_win_race_id = driver_data[driver_data['positionOrder'] == 1]['raceId'].max()
        races_from_last_win = driver_data[driver_data['raceId'] > last_win_race_id]['raceId'].count() if pd.notna(last_win_race_id) else None
        # Career Crashes
        career_crashes = driver_data[driver_data['statusId'].isin(crash_status_ids)]['statusId'].count()
        
        # append driver metrics
        driver_metrics.append({
            'driverId': driver_id,
            'Career Points': career_points,
            'Career Wins': career_wins,
            'Career Poles': career_poles,
            'Average Position Finish': avg_position_finish,
            'Average Qualifying': avg_qualifying,
            'Races': total_races,
            'Races to First Race Win': races_to_first_win,
            'Races from Last Race Win': races_from_last_win,
            'Career Crashes': career_crashes
        })


    # convert to DataFrame
    driver_analysis_df = pd.DataFrame(driver_metrics)

    # merge with driver names
    driver_analysis_df = pd.merge(driver_analysis_df, drivers_data, on='driverId')
    st.write(
        """
        This analysis presents key driver performance metrics—such as wins, points, and race entries—filtered dynamically by the selected season or aggregated across all seasons. The selected year decides which drivers are part of the comparison based on who raced that season. Even though a driver’s total career numbers don’t change, picking a specific year shifts the rankings and shows you who stood out during that time. This provides a season-specific perspective, allowing fans, analysts, and teams to focus on the standout drivers of a particular season while still considering both season-specific and career-long performance in Formula 1.
        """
    )
    st.markdown(
        f"""
        <hr style="border: 2px solid {'#E30613'}; margin: 30px 0;"/>
        """,
        unsafe_allow_html=True,
    )
        
    top_10_driver_by_points(driver_analysis_df, selected_year)

if __name__ == "__main__":
    driver_analysis_page()
