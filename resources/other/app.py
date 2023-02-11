import streamlit as st
import argparse
from colorama import Fore, Style
import pandas as pd
from Utils.Dictionaries import team_index_current
from Utils.tools import create_todays_games_from_odds, get_json_data, to_data_frame, get_todays_games_json, create_todays_games
from OddsProvider.SbrOddsProvider import SbrOddsProvider


todays_games_url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2022/scores/00_todays_scores.json'
todays_games_url_nhl = ''
data_url = 'https://stats.nba.com/stats/leaguedashteamstats?' \
           'Conference=&DateFrom=&DateTo=&Division=&GameScope=&' \
           'GameSegment=&LastNGames=0&LeagueID=00&Location=&' \
           'MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&' \
           'PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&' \
           'PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&' \
           'Season=2022-23&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&' \
           'StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='

def createTodaysGames(games, df, odds):
    match_data = []
    todays_games_uo = []
    home_team_odds = []
    away_team_odds = []

    for game in games:
        home_team = game[0]
        away_team = game[1]
        if odds is not None:
            game_odds = odds[home_team + ':' + away_team]
            todays_games_uo.append(game_odds['under_over_odds'])
            
            home_team_odds.append(game_odds[home_team]['money_line_odds'])
            away_team_odds.append(game_odds[away_team]['money_line_odds'])

        else:
            todays_games_uo.append(input(home_team + ' vs ' + away_team + ': '))

            home_team_odds.append(input(home_team + ' odds: '))
            away_team_odds.append(input(away_team + ' odds: '))

        home_team_series = df.iloc[team_index_current.get(home_team)]
        away_team_series = df.iloc[team_index_current.get(away_team)]
        stats = pd.concat([home_team_series, away_team_series])
        match_data.append(stats)

    games_data_frame = pd.concat(match_data, ignore_index=True, axis=1)
    games_data_frame = games_data_frame.T

    frame_ml = games_data_frame.drop(columns=['TEAM_ID', 'CFID', 'CFPARAMS', 'TEAM_NAME'])
    data = frame_ml.values
    data = data.astype(float)

    return data, todays_games_uo, frame_ml, home_team_odds, away_team_odds


def getOdds(sportsbook):
    odds = None
    print(f' sportsbook is {sportsbook} ----------- \n')
    if sportsbooks != None:
        odds = SbrOddsProvider(sportsbook).get_odds()
        games = create_todays_games_from_odds(odds)
        if((games[0][0]+':'+games[0][1]) not in list(odds.keys())):
            print(games[0][0]+':'+games[0][1])
            print(Fore.RED, "--------------Games not up to date for todays games. Scraping disabled until list is updated.--------------")
            print(Style.RESET_ALL)
            odds = None
        else:
            print(f"------------------{sportsbook} odds data------------------")
            for g in odds.keys():
                home_team, away_team = g.split(":")
                print(f"{away_team} ({odds[g][away_team]['money_line_odds']}) @ {home_team} ({odds[g][home_team]['money_line_odds']})")
    else:
        print('Please select sportsbook')
        data = get_todays_games_json(todays_games_url)
        games = create_todays_games(data)
    data = get_json_data(data_url)
    df = to_data_frame(data)
    data, todays_games_uo, frame_ml, home_team_odds, away_team_odds = createTodaysGames(games, df, odds)
    return data, todays_games_uo, frame_ml, home_team_odds, away_team_odds, odds
    

   
st.markdown("# Welcome to distributed online betting platform...")
st.markdown("## Bet now!")
st.text(" \n")
sportsbooks = ['fanduel', 'draftkings', 'betmgm', 'pointsbet', 'caesars', 'wynn', 'bet_rivers_ny']
sportsbook = st.selectbox('Select the sports book to fetch from', sportsbooks)
data, todays_games_uo, frame_ml, home_team_odds, away_team_odds, odds = getOdds(sportsbook)
st.text(" \n")
bet_amounts = {}
counter=1;
for g in odds.keys():
    home_team, away_team = g.split(":")
    st.write(f"{away_team} ({odds[g][away_team]['money_line_odds']}) @ {home_team} ({odds[g][home_team]['money_line_odds']})")
    st.text(" \n")
    input_str = f"Bet Amount {counter}"
    bet_amounts["bet_amount_{0}".format(counter)] = st.number_input(input_str)
    st.text(" \n")
    counter = counter+1
    
if st.button("Submit"):
    st.write(bet_amounts)
    st.balloons()