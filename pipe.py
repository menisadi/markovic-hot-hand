from basketball_reference_scraper.shot_charts import get_shot_chart
from basketball_reference_scraper.seasons import get_schedule
import pandas as pd
import time

def schedule(team, years, sleep_time=30):
  print(f'Team: {team}')
  full_schedule = pd.DataFrame()
  for i in years:
    schedule_i = get_schedule(i, playoffs=False)
    home = schedule_i.loc[schedule_i['HOME'] == team]
    away = schedule_i.loc[schedule_i['VISITOR'] == team]
    frames = [home, away]
    year_team = pd.concat(frames)
    print(f'year - {i}')
    time.sleep(sleep_time)
    frames = [full_schedule, year_team]
    full_schedule = pd.concat(frames)
  return full_schedule.sort_values(by=['DATE']).reset_index()

def empty_game_df():
  empty_df = pd.DataFrame(columns=['x', 'y', 'QUARTER', 'TIME_REMAINING', 'PLAYER', 'MAKE_MISS', 'VALUE', 'DISTANCE', 'team'])
  return empty_df

def get_shots(game_df, empty_df, team, sleep_time=30):
  home = list(game_df['HOME'])
  away = list(game_df['VISITOR'])
  # dates = [date.strftime('%Y-%m-%d') for date in list(game_df['DATE'])]
  dates = game_df['DATE']
  for i in range(len(dates)):
    print('-' * 50)
    print(dates[i])
    print(f'{home[i]} vs. {away[i]}')
    temp_dic = get_shot_chart(dates[i], home[i], away[i])
    print('got game')
    brk_df = temp_dic[team]
    frames = [empty_df, brk_df]
    empty_df =pd.concat(frames)
    time.sleep(sleep_time)
  return empty_df

def get_player_shots(player, shots_df):
  return shots_df.loc[shots_df['PLAYER'] == player]

def team_shorten(team_name):
    team_dict = {'ATLANTA HAWKS': 'ATL', 'BOSTON CELTICS': 'BOS', 'BROOKLYN NETS': 'BRK', 'CHICAGO BULLS': 'CHI', 'CHARLOTTE HORNETS': 'CHO', 'CLEVELAND CAVALIERS': 'CLE',
                'DALLAS MAVERICKS': 'DAL', 'DENVER NUGGETS': 'DEN', 'DETROIT PISTONS': 'DET', 'GOLDEN STATE WARRIORS': 'GSW', 'HOUSTON ROCKETS': 'HOU',
                'INDIANA PACERS': 'IND', 'LOS ANGELES CLIPPERS': 'LAC', 'LOS ANGELES LAKERS': 'LAL', 'MEMPHIS GRIZZLIES': 'MEM', 'MIAMI HEAT': 'MIA', 
                'MILWAUKEE BUCKS': 'MIL', 'MINNESOTA TIMBERWOLVES': 'MIN', 'NEW ORLEANS PELICANS': 'NOP', 'NEW YORK KNICKS': 'NYK', 'OKLAHOMA CITY THUNDER': 'OKC',
                'ORLANDO MAGIC': 'ORL', 'PHILADELPHIA 76ERS': 'PHI', 'PHOENIX SUNS': 'PHO', 'PORTLAND TRAIL BLAZERS': 'POR', 'SACRAMENTO KINGS': 'SAC',
                'SAN ANTONIO SPURS': 'SAS', 'TORONTO RAPTORS': 'TOR', 'UTAH JAZZ': 'UTA', 'WASHINGTON WIZARDS': 'WAS'}
    return team_dict[team_name]

def get_player_csv(team, years, player, sleep_time=30):
  '''
  inputs: 
  1. team - full name of NBA team (str)
  2. years - list of years (list)
  3. player - full name of a player (str)

  output:
  1. player_shots - csv containing the player shots over the years in the list
                    while he was in the team 
  '''
  print('Start Scrapping Schedule...')
  schedule_df = schedule(team, years, sleep_time) # get team games
  empty_df = empty_game_df() # build empty shots df
  print('Start Scarpping Shots...')
  shots_df = get_shots(schedule_df, empty_df, team_shorten(team.upper()), sleep_time) # get full shots of team
  print('Seperate Player...')
  player_shots = get_player_shots(player, shots_df) # seperate the df to get player shots
  return player_shots
