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
from Utils.tools import create_todays_games_from_odds, get_json_data, to_data_frame, get_todays_games_json, create_todays_games,payout
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

class Bet:
    def __init__(self, sportsbook, game, team, bet_type, odds):
        self.sportsbook = sportsbook
        self.game = game
        self.team = team
        self.bet_type = bet_type
        self.odds = odds
    
# Data Sources
@st.cache(ttl=600)
def getOdds(sportsbook):
    odds = None
    if sportsbooks != None:
        print('\n')
        print('-------------')
        print(sportsbook)
        odds,dict_games = SbrOddsProvider(sportsbook).get_odds()
        print(odds)
    else:
        print('Please select sportsbook')

    data = get_json_data(data_url)
    df = to_data_frame(data)
    #data, todays_games_uo, frame_ml, home_team_odds, away_team_odds = createTodaysGames(games, df, odds)
    return df, odds,dict_games

if 'user_bets' not in st.session_state:
    st.session_state['user_bets'] = []
    
def add_bet(sportsbook, game, team, bet_type, odds):
    st.session_state.user_bets.append(Bet(sportsbook, game, team, bet_type, odds))


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
        df, odds, dict_games = getOdds(sportsbook)
        df1 = pd.DataFrame.from_dict(dict_games).T

        #Team list
        games = df1['game'].unique()


        # Filter for teams
        game_options = st.multiselect(
            '**Select your matches(s):**',
            options=games,
            default=games[1],
            key= f'game_options_{sportsbook}'
        )

        counter = 0
        with st.container():
            cl1, cl2, cl3,cl4= st.columns(4, gap="medium")
            with cl1:
                st.subheader("Team Names")
            with cl2:
                st.subheader("Moneyline")
            with cl3:
                st.subheader("Spread")
            with cl4:
                st.subheader("Total")

        for game in game_options:
            df2 = df1[df1['game']==game]
            counter = df1[df1['game']==game].index.values[0]
            with st.container():
                st.write('---')
                #st.subheader(df2.game[counter])
                with st.container():
                    c1, c2, c3,c4= st.columns(4, gap="medium")
                    with c1:
                        st.write(df2.home_team[counter])
                    with c2:
                        st.button(
                            f"{df2.home_ml_odds[counter]}", 
                            key=f"{sportsbook}_{df2.home_team[counter]}_ml_{counter}", 
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.home_team[counter],"ML",df2.home_ml_odds[counter], )
                        )
                    with c3:
                        st.button(
                            f"{df2.home_spread[counter]}", 
                            key=f"{sportsbook}_{df2.home_team[counter]}_s_{counter}",
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.home_team[counter],"Spread",df2.home_spread[counter], )
                        )
                    with c4:
                        st.button(
                            f"{df2.home_total[counter]}", 
                            key=f"{sportsbook}_{df2.home_team[counter]}_t_{counter}",
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.home_team[counter],"Total",df2.home_total[counter], )
                        )
                with st.container():
                    c1, c2, c3,c4= st.columns(4, gap="medium")
                    with c1:
                        st.write(df2.away_team[counter])
                    with c2:
                        st.button(
                            f"{df2.away_ml_odds[counter]}", 
                            key=f"{sportsbook}_{df2.away_team[counter]}_ml_{counter}",
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.away_team[counter],"ML",df2.away_ml_odds[counter], )
                        )

                    with c3:
                        st.button(
                            f"{df2.away_spread[counter]}", 
                            key=f"{sportsbook}_{df2.away_team[counter]}_s_{counter}",
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.away_team[counter],"Spread",df2.away_spread[counter], )
                        )
                    with c4:
                        st.button(
                            f"{df2.away_total[counter]}", 
                            key=f"{sportsbook}_{df2.away_team[counter]}_t_{counter}",
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.away_team[counter],"Total",df2.away_total[counter], )
                        )
   
st.sidebar.subheader("User Bet Slip")
for bet in st.session_state.user_bets:
    st.sidebar.write(bet.game)
    st.sidebar.write(bet.team)
    st.sidebar.write(bet.bet_type)
    st.sidebar.write(st.number_input("amount", key=f"bet_amount_{bet}"))
    st.sidebar.write(payout(st.session_state[f"bet_amount_{bet}"],bet.odds))