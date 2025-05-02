import pandas as pd

# Paths to data files
seasons_file = 'data/seasons.csv'
races_file = 'data/races.csv'
results_file = 'data/results.csv'
driver_standings_file = 'data/driver_standings.csv'
drivers_file = 'data/drivers.csv'


# Drivers Standings based on Year
def driversStandingsDf(year):
    races_data = pd.read_csv(races_file)
    driver_standings_data = pd.read_csv(driver_standings_file)
    drivers_data = pd.read_csv(drivers_file)

    selected_races = races_data[races_data['year'] == year]
    last_race_id = selected_races.loc[selected_races['round'].idxmax(), 'raceId']
    selected_driver_standings = driver_standings_data[driver_standings_data['raceId'] == last_race_id]
    selected_drivers = drivers_data[drivers_data['driverId'].isin(selected_driver_standings['driverId'])]
    
    # Merge driver standings with driver details
    drivers_standings_df = selected_driver_standings.merge(
        selected_drivers, on='driverId', how='inner'
    )
    drivers_standings_df['Driver Full Name'] = drivers_standings_df['forename'] + " " + drivers_standings_df['surname']
    drivers_standings_df = drivers_standings_df.sort_values(by='position')
    
    return selected_driver_standings, selected_drivers


def wroldChampionshipDataDf():
    seasons_data = pd.read_csv(seasons_file)
    races_data = pd.read_csv(races_file)
    driver_standings_data = pd.read_csv(driver_standings_file)
    
    world_championship_data = []
    for year in seasons_data['year']:
        year_races = races_data[races_data['year'] == year]
        last_round = year_races['round'].max()
        last_race_id = year_races[year_races['round'] == last_round]['raceId'].iloc[0]
        year_results = driver_standings_data[driver_standings_data['raceId'] == last_race_id]
        max_points_driver = year_results.loc[year_results['points'].idxmax(), 'driverId']
        world_championship_data.append({'Year': year, 'Last Round': last_round, 'Last Race ID': last_race_id, 'Driver ID': max_points_driver})
    world_championship_df = pd.DataFrame(world_championship_data)

    return world_championship_df
