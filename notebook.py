# -*- coding: utf-8 -*-

#pobranie sezonow (era hybrydowa od 2014 roku na tej bazujemy)
import requests
import pandas as pd

url = "http://ergast.com/api/f1/seasons.json?limit=1000"
response = requests.get(url)
data = response.json()

seasons = data['MRData']['SeasonTable']['Seasons']

season_list = [int(season['season']) for season in seasons]

df_seasons = pd.DataFrame(season_list, columns=['season'])
year_of_hybrid_era = 2014
hybrid_era_seasons = [season for season in season_list if season >= year_of_hybrid_era]
hybrid_era_seasons

#pobranie danych o konstruktorach dla każdego z wczesniej pobranych sezonow
from tqdm import tqdm

constructors_data = []

# Iteruj po sezonach
for season in tqdm(hybrid_era_seasons):
    url = f"http://ergast.com/api/f1/{season}/constructors.json?limit=100"
    response = requests.get(url)
    data = response.json()

    constructors = data['MRData']['ConstructorTable']['Constructors']

    for constructor in constructors:
        constructors_data.append({
            'season': season,
            'constructorId': constructor['constructorId'],
            'name': constructor['name'],
            'nationality': constructor['nationality']
        })

# Do DataFrame
df_constructors = pd.DataFrame(constructors_data)

# Przykładowe dane
df_constructors

import requests
import pandas as pd
from tqdm import tqdm
import time

# Punkty zespołu do danego GP
def get_constructor_points_upto_gp(season, round_, constructor_id):
    url = f"http://ergast.com/api/f1/{season}/{round_}/constructors/{constructor_id}/constructorStandings.json"
    response = requests.get(url)
    data = response.json()

    standings_list = data['MRData']['StandingsTable']['StandingsLists']
    if standings_list:
        for constructor in standings_list[0]['ConstructorStandings']:
            if constructor['Constructor']['constructorId'] == constructor_id:
                return float(constructor['points'])
    return 0.0


# Zliczanie zwycięstw konstruktorów

wins_data = []

for season in tqdm(hybrid_era_seasons, desc="Zliczanie zwycięstw"):
    for constructor_id in df_constructors[df_constructors['season'] == season]['constructorId'].unique():
        url = f"http://ergast.com/api/f1/{season}/constructors/{constructor_id}/results/1.json?limit=1000"
        response = requests.get(url)
        data = response.json()
        wins = len(data['MRData']['RaceTable']['Races'])
        wins_data.append({
            'season': season,
            'constructorId': constructor_id,
            'number_of_constructor_wins': wins
        })
        time.sleep(0.5)

df_wins = pd.DataFrame(wins_data)

df_final = df_constructors.merge(df_wins, on=['season', 'constructorId'], how='left')

df_final

#pobranie kierowcow

def get_drivers_from_season(season):
    url = f"http://ergast.com/api/f1/{season}/1/results.json?limit=100"
    response = requests.get(url)
    data = response.json()

    races = data['MRData']['RaceTable']['Races']
    if not races:
        return pd.DataFrame()

    results = races[0]['Results']

    drivers = []
    for result in results:
        driver = result['Driver']
        constructor = result['Constructor']

        drivers.append({
            'season': season,
            'driverId': driver['driverId'],
            'givenName': driver['givenName'],
            'familyName': driver['familyName'],
            'fullName': f"{driver['givenName']} {driver['familyName']}",
            'dateOfBirth': driver['dateOfBirth'],
            'nationality': driver['nationality'],
            'constructorId': constructor['constructorId'],
            'constructorName': constructor['name']
        })

    return pd.DataFrame(drivers)

drivers_2023 = get_drivers_from_season(2023)
drivers_2023

from datetime import datetime

def get_driver_career_stats(driver_id):
    url = f"http://ergast.com/api/f1/drivers/{driver_id}/results.json?limit=1000"
    response = requests.get(url)
    data = response.json()

    results = data['MRData']['RaceTable']['Races']
    if not results:
        return {
            'number_of_races': 0,
            'career_points': 0.0,
            'number_of_wins': 0,
            'number_of_podiums': 0,
            'debut_year': None
        }

    num_races = len(results)
    points = 0.0
    wins = 0
    podiums = 0
    debut_year = int(results[0]['season'])  # pierwszy sezon

    for race in results:
        result = race['Results'][0]
        position = result.get('position')
        points += float(result.get('points', 0))
        if position == '1':
            wins += 1
        if position and int(position) <= 3:
            podiums += 1

    return {
        'number_of_races': num_races,
        'career_points': points,
        'number_of_wins': wins,
        'number_of_podiums': podiums,
        'debut_year': debut_year
    }

career_stats = []

for _, row in drivers_2023.iterrows():
    stats = get_driver_career_stats(row['driverId'])
    career_stats.append(stats)

career_df = pd.DataFrame(career_stats)
drivers_with_career = pd.concat([drivers_2023, career_df], axis=1)

drivers_with_career

def get_all_races(start_season=2014, end_season=2024):
    races = []

    for season in range(start_season, end_season + 1):
        url = f"http://ergast.com/api/f1/{season}.json"
        response = requests.get(url)
        data = response.json()

        season_races = data['MRData']['RaceTable']['Races']
        for race in season_races:
            races.append({
                'season': int(season),
                'round': int(race['round']),
                'raceName': race['raceName'],
                'date': race['date'],
                'circuitId': race['Circuit']['circuitId'],
                'circuitName': race['Circuit']['circuitName'],
                'country': race['Circuit']['Location']['country']
            })

    return pd.DataFrame(races)

# Pobierz wszystkie wyścigi 2014–2024
all_races_df = get_all_races()
print(all_races_df.head())

# mozna wykorzystac all_races_df

def build_driver_features_for_each_race(start_year=2014, end_year=2023):
    all_rows = []
    driver_results_cache = {}

    for season in range(start_year, end_year + 1):
        for rnd in range(1, 25):
            race_url = f"http://ergast.com/api/f1/{season}/{rnd}/results.json?limit=100"
            response = requests.get(race_url)
            data = response.json()
            races = data['MRData']['RaceTable']['Races']
            if not races:
                break  # brak dalszych wyścigów

            race = races[0]
            race_date = race['date']
            race_results = race['Results']

            for result in race_results:
                driver = result['Driver']
                driver_id = driver['driverId']
                dob = driver['dateOfBirth']
                race_day = pd.to_datetime(race_date)
                age = (race_day - pd.to_datetime(dob)).days / 365.25

              # cache: jeśli brak danych, pobierz raz
                if driver_id not in driver_results_cache:
                    history_url = f"http://ergast.com/api/f1/drivers/{driver_id}/results.json?limit=1000"
                    hist_response = requests.get(history_url)
                    hist_data = hist_response.json()
                    hist_races = hist_data['MRData']['RaceTable']['Races']
                    driver_results_cache[driver_id] = hist_races
                else:
                    hist_races = driver_results_cache[driver_id]

                # Filtrowanie wyników przed danym GP
                past_races = [r for r in hist_races if r['date'] < race_date]
                past_races.sort(key=lambda r: r['date'], reverse=True)
                last_5 = past_races[:5]

                last_5_points = sum(float(r['Results'][0]['points']) for r in last_5) if last_5 else 0.0
                last_finish = int(past_races[0]['Results'][0]['position']) if past_races else None
                last_qualifying = int(past_races[0]['Results'][0].get('grid', 0)) if past_races else None
                final_position = int(result['position'])

                all_rows.append({
                    'season': season,
                    'round': rnd,
                    'race_date': race_date,
                    'driverId': driver_id,
                    'age_on_race_day': round(age, 2),
                    'last_5_race_points': last_5_points,
                    'last_race_finish': last_finish,
                    'last_qualifying_position': last_qualifying,
                    'final_position': final_position
                })

    return pd.DataFrame(all_rows)

drivers_stats = build_driver_features_for_each_race()

drivers_stats

import requests
import pandas as pd
from tqdm import tqdm
import time

# dane o kwalifikacjach i wyscigu dla kierowcy w konkretnym wyscigu
race_driver_data = []

for season in tqdm([2023], desc="Sezony"):
#for season in tqdm(hybrid_era_seasons, desc="Sezony"):
    races_in_season = all_races_df[all_races_df['season'] == season]

    for _, race in tqdm(races_in_season.iterrows(), desc=f"Wyścigi {season}", leave=False):
        round_ = race['round']
        race_name = race['raceName']
        date = race['date']

        # wyniki wyścigu
        url_race = f"http://ergast.com/api/f1/{season}/{round_}/results.json?limit=100"
        race_res = requests.get(url_race).json()
        try:
            results = race_res['MRData']['RaceTable']['Races'][0]['Results']
        except IndexError:
            continue

        # dane o kwalifikacjach dla danego wyścigu
        url_qual = f"http://ergast.com/api/f1/{season}/{round_}/qualifying.json"
        qual_res = requests.get(url_qual).json()
        try:
            qualifying_results = qual_res['MRData']['RaceTable']['Races'][0]['QualifyingResults']
        except IndexError:
            qualifying_results = []

        for result in results:
            driver = result['Driver']
            driver_id = driver['driverId']
            constructor_id = result['Constructor']['constructorId']
            grid = int(result['grid'])  # pozycja startowa
            finish_position = int(result['position'])  # pozycja na mecie
            status = result['status']  # status kierowcy

            finished = status.lower() in ['finished'] or 'lap' in status.lower()

            # dopasowanie pozycji kwalifikacyjnej
            qual_position = None
            for qual_result in qualifying_results:
                if qual_result['Driver']['driverId'] == driver_id:
                    qual_position = int(qual_result['position'])
                    break

            race_driver_data.append({
                'season': int(season),
                'round': int(round_),
                'race_name': race_name,
                'race_date': date,
                'driverId': driver_id,
                'constructorId': constructor_id,
                'grid': grid,
                'qual_position': qual_position,
                'finish_position': finish_position,
                'finished': int(finished)
            })

df_race_driver = pd.DataFrame(race_driver_data)

print(df_race_driver.head())

import requests
import pandas as pd
from tqdm import tqdm
import time

all_meetings = []

for year in tqdm(hybrid_era_seasons, desc="Pobieranie danych"):
    url = f"https://api.openf1.org/v1/meetings?year={year}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            gp_data = [m for m in data if "Grand Prix" in m.get("meeting_name", "")]
            filtered_gp_data = [
                {
                    'meeting_key': m.get('meeting_key'),
                    'circuit_key': m.get('circuit_key'),
                    'meeting_name': m.get('meeting_name'),
                    'year': m.get('year'),
                }
                for m in gp_data
            ]
            all_meetings.extend(filtered_gp_data)
        else:
            print(f"Błąd w roku {year}: status {response.status_code}")
    except Exception as e:
        print(f"Wyjątek w roku {year}: {e}")

    time.sleep(0.3)

# Zamień na DataFrame
df_meetings = pd.DataFrame(all_meetings)

# Podgląd danych
print(df_meetings.head())