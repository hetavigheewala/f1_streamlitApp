import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
from PIL import Image
from dataBank import world_driver_championship_df
import random


seasons_file = 'data/seasons.csv'
races_file = 'data/races.csv'
results_file = 'data/results.csv'
driver_standings_file = 'data/driver_standings.csv'
drivers_file = 'data/drivers.csv'
constructors_standings_file = 'data/constructor_standings.csv'
constructors_file = 'data/constructors.csv'
races_data = pd.read_csv(races_file)
results_data = pd.read_csv(results_file)
drivers_df = pd.read_csv(drivers_file)


def load_F1_image(file_path, size=(400, 155)):
    try:
        img = Image.open(file_path)
        img = img.resize(size)  
        return img
    except FileNotFoundError:
        return None

def top_10_driver_by_points(driver_analysis_df, selected_year):
    # filter races based on the selected year
    if selected_year == "All":
        selected_races = races_data
    else:
        selected_races = races_data[races_data['year'] == int(selected_year)]
    
    race_ids = selected_races['raceId'].tolist()

    selected_results_data = results_data[results_data['raceId'].isin(race_ids)]     # filter results to only include the selected races
    selected_drivers = selected_results_data['driverId'].unique()                   # get all unique driver IDs from the filtered results
    selected_drivers_analysis = driver_analysis_df[driver_analysis_df['driverId'].isin(selected_drivers)]       # filter the driver analysis DataFrame to only include the selected drivers
    top_drivers_df = selected_drivers_analysis.sort_values(by='Career Points', ascending=False).head(10)           # sort the filtered drivers by career points in descending order

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

    top_drivers_df['hover_text'] = top_drivers_df['number_x'] + " " + top_drivers_df['Name']

    chart = alt.Chart(top_drivers_df).mark_bar().encode(
            x=alt.X('code_x', sort=alt.EncodingSortField(field='Career Points', order='descending'), title=None),
            y=alt.Y('Career Points', title='Points'),
            color=alt.Color('Color', scale=None),
            tooltip=[
                alt.Tooltip('hover_text', title='Driver'),
                alt.Tooltip('Career Points', title='Points')
            ]
        ).properties(
            height=500,
            width=700
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_view(
            strokeWidth=0
        )

    # chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

    return top_drivers_df
def top_10_driver_by_world_championships(top_drivers_df, selected_year):
    st.markdown(
        f"""
            <div style="text-align: center; margin-left: -50px; font-size: 30px;  font-weight: bold; color: {'#E30613'};">
            Top 10 Drivers by Championship
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.write(
        """
            The Top 10 Drivers by Championships Analysis highlights the most successful drivers based on the total number of World Championships they have won. This analysis helps identify the elite performers who have reached the pinnacle of Formula 1 success, showcasing dominance across different eras. By examining championships won, it provides insights into drivers’ peak performance years and their ability to maintain top-level competitiveness.
        """
                )
    world_championship_df = world_driver_championship_df()
    driver_counts = world_championship_df['Driver ID'].value_counts().reset_index()
    
    # rename columns for clarity
    driver_counts.columns = ['driverId', 'championship']
    drivers_df['name'] = drivers_df['forename'] + " " + drivers_df['surname']

    #  new DataFrame with required columns
    new_df = pd.DataFrame()
    new_df['surname'] = drivers_df['surname']
    new_df['driverId'] = drivers_df['driverId']
    new_df['code'] = drivers_df['code']
    new_df['name'] = drivers_df['name']
    new_df['number'] = drivers_df['number']

    #  dictionary for quick lookup from driverId -> championship count
    championship_dict = dict(zip(driver_counts['driverId'], driver_counts['championship']))
    new_df['championship'] = new_df['driverId'].map(championship_dict).fillna(0).astype(int)        # .map() to fill championship values, default 0 if driverId not present

    if selected_year == "All":
        selected_races = races_data
    else:
        selected_races = races_data[races_data['year'] == int(selected_year)]
    
    race_ids = selected_races['raceId'].tolist()

    selected_results_data = results_data[results_data['raceId'].isin(race_ids)]                         # filter results to only include the selected races
    selected_drivers = selected_results_data['driverId'].unique()                                       # get all unique driver IDs from the filtered results
    selected_drivers_analysis = new_df[new_df['driverId'].isin(selected_drivers)]                       # filter the driver analysis DataFrame to only include the selected drivers
    top_drivers = selected_drivers_analysis.sort_values(by='championship', ascending=False).head(10)    # sort the filtered drivers by career points in descending order
    color_mapping = dict(zip(top_drivers_df['driverId'], top_drivers_df['Color']))
    top_drivers['Color'] = top_drivers['driverId'].map(color_mapping)

    chart = alt.Chart(top_drivers).mark_bar().encode(
        x=alt.X(
            'surname',
            sort=alt.EncodingSortField(field='championship', order='descending'),
            title=None,
            axis=alt.Axis(labelAngle=-45)  
        ),
        y=alt.Y(
            'championship',
            title='Championships',
            scale=alt.Scale(domain=[0, top_drivers['championship'].max() + 1]), 
            axis=alt.Axis(tickMinStep=1)                                  
        ),
        color=alt.Color('Color', scale=None),
        tooltip=[
            alt.Tooltip('name', title='Driver'),
            alt.Tooltip('championship', title='Championships')
        ]
    ).properties(
        height=500,
        width=700
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_view(
        strokeWidth=0
    )
    st.altair_chart(chart, use_container_width=True)
def top_10_driver_by_wins(top_drivers_df):
    
    st.markdown(
        f"""
            <div style="text-align: center; margin-left: -50px; font-size: 30px;  font-weight: bold; color: {'#E30613'};">
            Top 10 Drivers by Wins
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write(
        """
        The Top 10 Drivers by Wins analysis provides valuable insights into driver performance by highlighting those with the highest career victories. For analysts and teams, it offers a clear view of consistency and success, helping to identify patterns in winning strategies and the impact of various factors like car performance and team dynamics. This data can guide decisions on driver recruitment, team investments, and race strategies. Fans benefit by gaining a deeper appreciation for the sport’s history and understanding what sets top drivers apart. By combining historical data with actionable insights, this analysis bridges performance trends with the competitive spirit of Formula 1.
        """
        )
    top_10_wins= top_drivers_df.sort_values(by='Career Wins', ascending=False).head(10)

    # map the colors to the drivers
    top_10_wins['hover_text'] = top_10_wins['number_x'] + " " + top_10_wins['Name']
    chart = alt.Chart(top_10_wins).mark_bar().encode(
            x=alt.X('surname_x', sort=alt.EncodingSortField(field='Career Wins', order='descending'), title=None,
            axis=alt.Axis(labelAngle=-45)  
        ),
            y=alt.Y('Career Wins', title='Career Wins'),
            color=alt.Color('Color', scale=None),
            tooltip=[
                alt.Tooltip('hover_text', title='Driver'),
                alt.Tooltip('Career Wins', title='Career Wins'),
                alt.Tooltip('number_x', title = 'Driver Number'),
                alt.Tooltip('code_x', title = 'Code')
            ]
        ).properties(
            height=500,
            width=700
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_view(
            strokeWidth=0
        )

    # chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
def top_10_driver_by_pole(top_drivers_df):
    st.markdown(
        f"""
            <div style="text-align: center; margin-left: -50px; font-size: 30px;  font-weight: bold; color: {'#E30613'};">
            Top 10 Drivers by Pole
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write(
        """
            In Formula 1, the pole position is awarded to the driver who achieves the fastest time in qualifying, something that demands precision, skill, and flawless execution under immense pressure. Securing pole is crucial as it offers a clear track, minimizes the risk of early collisions, and provides a psychological advantage over competitors. The Top 10 Drivers by Pole analysis shows which drivers excel in qualifying and perform well under pressure. It helps teams spot patterns, improve strategies, and understand how drivers use strong starting positions to win races.   """
        )

    top_10_poles = top_drivers_df.sort_values(by='Career Poles', ascending=False).head(10)


    # map the colors to the drivers
    top_10_poles['hover_text'] = top_10_poles['number_x'] + " " + top_10_poles['Name']
    chart = alt.Chart(top_10_poles).mark_bar().encode(
            x=alt.X('surname_x', sort=alt.EncodingSortField(field='Career Poles', order='descending'), title=None,
            axis=alt.Axis(labelAngle=-45)  
        ),
            y=alt.Y('Career Poles', title='Career Poles'),
            color=alt.Color('Color', scale=None),
            tooltip=[
                alt.Tooltip('hover_text', title='Driver'),
                alt.Tooltip('Career Poles', title='Career Poles'),
                alt.Tooltip('number_x', title = 'Driver Number'),
                alt.Tooltip('code_x', title = 'Code')
            ]
        ).properties(
            height=500,
            width=700
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_view(
            strokeWidth=0
        )

    # chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
def top_10_driver_by_crashes(top_drivers_df):
    st.markdown(
        f"""
            <div style="text-align: center; margin-left: -50px; font-size: 30px;  font-weight: bold; color: {'#E30613'};">
            Top 10 Drivers by Career Crashes
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write(
        """
        The Top 10 Drivers by Career Crashes analysis highlights drivers with the highest crash rates, revealing important patterns in risk-taking and driving style. Crashes can heavily impact race outcomes, team finances, and car repairs, making this data valuable for improving strategies and safety measures. This analysis showcases how understanding crash trends can help teams make smarter decisions to boost performance and reduce risks on the track.
        """
        )

    top_10_crashers = top_drivers_df.sort_values(by='Career Crashes', ascending=False).head(10)

    # map the colors to the drivers
    top_10_crashers['hover_text'] =  top_10_crashers['Name'] 
    chart = alt.Chart(top_10_crashers).mark_bar().encode(
            x=alt.X('surname_x', sort=alt.EncodingSortField(field='Career Crashes', order='descending'), title=None,
            axis=alt.Axis(labelAngle=-45)  
        ),
            y=alt.Y('Career Crashes', title='Career Crashes'),
            color=alt.Color('Color', scale=None),
            tooltip=[
                alt.Tooltip('hover_text', title='Driver'),
                alt.Tooltip('Career Crashes', title='Career Crashes'),
                alt.Tooltip('number_x', title = 'Driver Number'),
                alt.Tooltip('code_x', title = 'Code')
            ]
        ).properties(
            height=500,
            width=700
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_view(
            strokeWidth=0
        )
    st.altair_chart(chart, use_container_width=True)
def top_10_driver_without_wins(driver_analysis_df):
    drivers_without_wins = driver_analysis_df[driver_analysis_df['Career Wins'] == 0]
    drivers_without_wins_sorted = drivers_without_wins.sort_values(by='Races', ascending=False)         # sort by number of races in descending order
    top_10_drivers_without_wins = drivers_without_wins_sorted.head(10)                                  # select top 10 drivers who have done the most races without any wins
    
    st.markdown(
        f"""
            <div style="text-align: center; margin-left: -50px; font-size: 30px;  font-weight: bold; color: {'#E30613'};">
            Top 10 Drivers by Without Wins
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write(
        """
        The Top 10 Drivers Without Wins analysis focuses on drivers with the most races but no victories, highlighting their commitment and consistency. This analysis is valuable for uncovering patterns in performance and understanding factors beyond wins, such as teamwork and strategy. It demonstrates strong analytical skills by using data to evaluate talent and identify areas for improvement in Formula 1 decision-making.
        """
    )
    top_10_drivers_without_wins['hover_text'] =  top_10_drivers_without_wins['Name']
    chart = alt.Chart(top_10_drivers_without_wins).mark_bar().encode(
        x=alt.X('surname_y', sort=alt.EncodingSortField(field='Races', order='descending'), title=None,
            axis=alt.Axis(labelAngle=-45)  
        ),
        y=alt.Y('Races', title='Number of Races without wins'),  
        color=alt.Color('Color', scale=None), 
        tooltip=[
            alt.Tooltip('hover_text', title='Driver'),  
            alt.Tooltip('number_y', title='Driver Number'), 
            alt.Tooltip('code_y', title='Code')  
        ]
    ).properties(
        height=500,
        width=700
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_view(
        strokeWidth=0
    )
    st.altair_chart(chart, use_container_width=True)
    
def driver_analysis_page():

    # header with logo
    logo_file = os.path.join("asset/f1_red.png")
    team_logo = load_F1_image(logo_file)
    
    cols = st.columns([1, 5])
    with cols[0]:
        st.markdown("<br>", unsafe_allow_html=True) 
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
    
    color_scheme = [
    # Blues
    '#4781D7', '#00A1E8', '#295294', '#1868DB', '#6C98FF',
    '#041E42', '#00A3E0', '#223971', '#0078C1', '#005BA9', '#499BCC',
    # Neutrals
    '#9C9FA2', '#C6C6C6', '#FFFFFF', '#00352F', '#00594F', '#1A6598',
    # Oranges
    '#F47600', '#FF8000',
    # Yellows
    '#FFEB00', '#FFC906',
    # unique
    '#47C7FC', '#981E32',
    # Pinks and Purples
    '#FD4BC7',
    # Reds
    '#A6051A', '#DB0A40', '#CC1E4A', '#ED1131', '#E40046', '#80142B', '#F62039',
    # Greens
    '#00D7B6', '#229971', '#01C00E', '#00A19C', '#CEDC00'
    ]
    crash_status_ids = [3, 4, 104, 130]                                # create analysis database

    results_data = pd.read_csv(results_file)
    drivers_data = pd.read_csv(drivers_file)

    driver_metrics = []                                                 # empty list to store driver metrics
    unique_driver_ids = results_data['driverId'].unique()               # unique driver IDs

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

    driver_analysis_df = pd.DataFrame(driver_metrics)               # convert to DataFrame
    driver_analysis_df['Color'] = [
        color_scheme[driver_id % len(color_scheme)] for driver_id in driver_analysis_df['driverId']
    ]

    driver_analysis_df = driver_analysis_df.merge(                                  # merge driver details from drivers_data into the analysis DataFrame
        drivers_data[['driverId', 'code', 'forename', 'surname', 'number']],
        on='driverId',
        how='left'
    )
    driver_analysis_df['Name'] = driver_analysis_df['forename'] + " " + driver_analysis_df['surname']           # add a full name column

    driver_analysis_df = driver_analysis_df[[               # rearrange columns for better readability
        'driverId', 'code', 'Name', 'number', 'Career Points', 'Career Wins', 'surname',
        'Career Poles', 'Average Position Finish', 'Average Qualifying',
        'Races', 'Races to First Race Win', 'Races from Last Race Win',
        'Career Crashes', 'Color'
    ]]

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
    top_drivers_df = top_10_driver_by_points(driver_analysis_df, selected_year)
    st.markdown(
        f"""
        <hr style="border: 2px solid {'#E30613'}; margin: 30px 0;"/>
        """,
        unsafe_allow_html=True,
    )
    top_10_driver_by_world_championships(driver_analysis_df, selected_year)
    st.markdown(
        f"""
        <hr style="border: 2px solid {'#E30613'}; margin: 30px 0;"/>
        """,
        unsafe_allow_html=True,
    )
    top_10_driver_by_wins(driver_analysis_df)
    st.markdown(
        f"""
        <hr style="border: 2px solid {'#E30613'}; margin: 30px 0;"/>
        """,
        unsafe_allow_html=True,
    )
    top_10_driver_by_pole(driver_analysis_df)
    st.markdown(
        f"""
        <hr style="border: 2px solid {'#E30613'}; margin: 30px 0;"/>
        """,
        unsafe_allow_html=True,
    )
    top_10_driver_by_crashes(driver_analysis_df)
    st.markdown(
        f"""
        <hr style="border: 2px solid {'#E30613'}; margin: 30px 0;"/>
        """,
        unsafe_allow_html=True,
    )
    top_10_driver_without_wins(driver_analysis_df)
      
    
if __name__ == "__main__":
    driver_analysis_page()
