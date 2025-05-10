import pandas as pd

# Paths to data files
seasons_file = 'data/seasons.csv'
races_file = 'data/races.csv'
results_file = 'data/results.csv'
driver_standings_file = 'data/driver_standings.csv'
drivers_file = 'data/drivers.csv'
constructors_standings_file = 'data/constructor_standings.csv'
constructors_file = 'data/constructors.csv'


# Drivers Standings based on Year
def driversStandingsDf(year):
    races_data = pd.read_csv(races_file)
    driver_standings_data = pd.read_csv(driver_standings_file)
    drivers_data = pd.read_csv(drivers_file)

    selected_races = races_data[races_data['year'] == year]
    last_race_id = selected_races.loc[selected_races['round'].idxmax(), 'raceId']
    selected_driver_standings = driver_standings_data[driver_standings_data['raceId'] == last_race_id]
    selected_drivers = drivers_data[drivers_data['driverId'].isin(selected_driver_standings['driverId'])]

    return selected_driver_standings, selected_drivers

def constructorStandingsDf(year):
    races_data = pd.read_csv(races_file)
    constructors_standings_data = pd.read_csv(constructors_standings_file)
    constructors_data = pd.read_csv(constructors_file)
    selected_races = races_data[races_data['year'] == year]
    last_race_id = selected_races.loc[selected_races['round'].idxmax(), 'raceId']
    selected_constructors_standings = constructors_standings_data[constructors_standings_data['raceId'] == last_race_id]
    selected_constructors = constructors_data[constructors_data['constructorId'].isin(selected_constructors_standings['constructorId'])]
    
    return selected_constructors_standings, selected_constructors



def world_driver_championship_df():
    seasons_data = pd.read_csv(seasons_file)
    races_data = pd.read_csv(races_file)
    driver_standings_data = pd.read_csv(driver_standings_file)
    
    world_driver_championship_data = []
    for year in seasons_data['year']:
        year_races = races_data[races_data['year'] == year]
        last_round = year_races['round'].max()
        last_race_id = year_races[year_races['round'] == last_round]['raceId'].iloc[0]
        year_results = driver_standings_data[driver_standings_data['raceId'] == last_race_id]
        max_points_driver = year_results.loc[year_results['points'].idxmax(), 'driverId']
        world_driver_championship_data.append({'Year': year, 'Last Round': last_round, 'Last Race ID': last_race_id, 'Driver ID': max_points_driver})
    world_driver_championship_df = pd.DataFrame(world_driver_championship_data)

    return world_driver_championship_df


def world_constructors_championship_df():
    seasons_data = pd.read_csv(seasons_file)
    races_data = pd.read_csv(races_file)    
    constructors_standings_data = pd.read_csv(constructors_standings_file)
    
    world_constructors_championship_data = []
    for year in seasons_data['year']:
        year_races = races_data[races_data['year'] == year]
        last_round = year_races['round'].max()
        last_race_id = year_races[year_races['round'] == last_round]['raceId'].iloc[0]
        year_results = constructors_standings_data[constructors_standings_data['raceId'] == last_race_id]
        
        if not year_results.empty and 'points' in year_results.columns and not year_results['points'].isna().all():
            max_points_constructor = year_results.loc[year_results['points'].idxmax(), 'constructorId']
        else:
            max_points_constructor = None  # handle the case where no constructor points are found
        
        world_constructors_championship_data.append({
            'Year': year,
            'Last Round': last_round,
            'Last Race ID': last_race_id,
            'Constructor ID': max_points_constructor
        })
    
    world_constructors_championship_df = pd.DataFrame(world_constructors_championship_data)
    return world_constructors_championship_df