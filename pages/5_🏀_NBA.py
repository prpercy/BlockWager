# Libraries
import streamlit as st
from streamlit_elements import elements, mui, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import argparse
from colorama import Fore, Style
from Utils.Dictionaries import team_index_current
from Utils.tools import create_todays_games_from_odds, get_json_data, to_data_frame, get_todays_games_json, create_todays_games
from OddsProvider.SbrOddsProvider import SbrOddsProvider

# Global Variables
theme_plotly = None # None or streamlit
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Layout
st.set_page_config(page_title='NBA Odds and Bets', page_icon=':bar_chart:', layout='wide')
st.title('🌍 NBA Odds and Bets')

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




# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


#Sportsbook list
sportsbooks = ['fanduel', 'draftkings', 'betmgm', 'pointsbet', 'caesars', 'wynn', 'bet_rivers_ny']

# Filter the sportsbooks
options = st.multiselect(
    '**Select your desired sportsbook(s):**',
    options=sportsbooks,
    default='fanduel',
    key='sportsbook_options'
)

#Team list
nba_teams = [
    "Atlanta Hawks",    "Boston Celtics",    "Brooklyn Nets",    "Charlotte Hornets",    "Chicago Bulls",
    "Cleveland Cavaliers",    "Dallas Mavericks",    "Denver Nuggets",    "Detroit Pistons",    "Golden State Warriors",
    "Houston Rockets",    "Indiana Pacers",    "Los Angeles Clippers",    "Los Angeles Lakers",    "Memphis Grizzlies",
    "Miami Heat",    "Milwaukee Bucks",    "Minnesota Timberwolves",    "New Orleans Pelicans",    "New York Knicks",
    "Oklahoma City Thunder",    "Orlando Magic",    "Philadelphia 76ers",    "Phoenix Suns",    "Portland Trail Blazers",
    "Sacramento Kings",    "San Antonio Spurs",    "Toronto Raptors",    "Utah Jazz",    "Washington Wizards"]


# Filter for teams
options = st.multiselect(
    '**Select your team(s):**',
    options=nba_teams,
    default=nba_teams,
    key='NBA Teams'
)
    
# Data Sources
@st.cache(ttl=600)
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
    if sportsbooks != None:
        print('\n')
        print('-------------')
        print(sportsbook)
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





st.markdown("""
<style>
div.stButton > button:first-child {
    box-shadow:inset 0px 39px 0px -24px #e67a73;
	background-color:#e4685d;
	border-radius:4px;
	border:1px solid #ffffff;
	display:inline-block;
	cursor:pointer;
	color:#ffffff;
	font-family:Arial;
	font-size:16px;
	padding:6px 15px;
	text-decoration:none;
	text-shadow:0px 1px 0px #b23e35;
    width: 100px;
}
</style>""", unsafe_allow_html=True)

# Present Odds to Client
if len(options) == 0:
    st.warning('Please select at least one sportsbook.')
else:
    
    
    for i in range(len(options)):
        sportsbook = options[i]
        st.subheader(f"Overview for {sportsbook} sportsbook")
        data, todays_games_uo, frame_ml, home_team_odds, away_team_odds, odds = getOdds(sportsbook)
        st.text(" \n")
        bet_amounts = {}
        counter=1;
        for g in odds.keys():
            home_team, away_team = g.split(":")
            c1, c2, c3,c4 = st.columns([3,2,2,4])
            with c1:
                st.write(f"{away_team}")
                if st.button(f"{odds[g][away_team]['money_line_odds']}", key=f"{sportsbook}_{away_team}_{counter}"):
                    st.write(f"betting on {away_team}")
                    st.balloons()
            with c2:
                st.write(f"{home_team}")
                if st.button(f"{odds[g][home_team]['money_line_odds']}", key=f"{sportsbook}_{home_team}_{counter}"):
                    st.write(f"betting on {home_team}")
                    st.balloons()
            with c3:
                input_str = f"Bet Amount {sportsbook} {counter}"
                bet_amounts["bet_amount_{0}_{1}".format(sportsbook,counter)] = st.number_input(input_str)
            with c4:
                st.text(" \n")
                st.text(" \n")
                
            counter = counter+1
            st.write('---')
            

        if st.button("Submit bets for {0}".format(sportsbook)):
            st.write(bet_amounts)
            st.balloons()
        st.text(" \n")
        with elements("nested_children"):
            with mui.Paper:
                with mui.Typography:
                    html.p(sportsbook)
                    html.p("Goodbye world")
            with mui.Paper(elevation=3, variant="outlined", square=True):
                mui.Typography(sportsbook)

 
