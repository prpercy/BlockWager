# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import argparse
from colorama import Fore, Style
from Utils.Dictionaries import team_index_current
from Utils.tools import create_todays_games_from_odds, get_json_data, to_data_frame, get_todays_games_json, create_todays_games,payout
from OddsProvider.SbrOddsProvider import SbrOddsProvider

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
        self.amount=0
    def update_bet(self, amount):
        self.amount = amount
    
# Data Sources
@st.cache(ttl=600)
def getOdds(sportsbook):
    odds = None
    if sportsbooks != None:
        print('\n')
        print('-------------')
        print(sportsbook)
        dict_games = SbrOddsProvider(sportsbook).get_odds()
        #print(odds)
    else:
        print('Please select sportsbook')

    data = get_json_data(data_url)
    df = to_data_frame(data)
    #data, todays_games_uo, frame_ml, home_team_odds, away_team_odds = createTodaysGames(games, df, odds)
    return df, dict_games

if 'user_bets' not in st.session_state:
    st.session_state['user_bets'] = []
    
def add_bet(sportsbook, game, team, bet_type, odds):
    if odds != "":
        st.session_state.user_bets.append(Bet(sportsbook, game, team, bet_type, odds))

def place_bets():
    st.sidebar.write("Bets placed:")
    for bet in st.session_state.user_bets:
        if f"bet_amount_{bet}" in st.session_state:
            print(f"you are updating bet with amount {st.session_state[f'bet_amount_{bet}']}")
            bet.update_bet(st.session_state[f'bet_amount_{bet}'])
            st.sidebar.write(f"{bet.sportsbook}-{bet.game}-{bet.team}-{bet.bet_type}-{bet.odds}-{bet.amount}")
    st.session_state['user_bets'] = []
   
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
    width: 130px;
    height: 52px;
}
</style>""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-baseweb=“base-input”] > div {
    height: 53px;
}
</style>""", unsafe_allow_html=True)

# Present Odds to Client
if len(options) == 0:
    st.warning('Please select at least one sportsbook.')
else:
    for i in range(len(options)):
        sportsbook = options[i]
        st.markdown("***")
        st.subheader(f"Overview for {sportsbook} sportsbook")
        df, dict_games = getOdds(sportsbook)
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
            c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns(9, gap="medium")
            with c1:
                st.write("")
            with c2:
                st.subheader("Teams")
            with c3:
                st.subheader("Moneyline")
            with c4:
                st.subheader("Spread")
            with c5:
                st.subheader("Total")
            with c6:
                st.subheader("Bets")
            with c7:
                st.button(label='Place bets', key=f"place_bets_{sportsbook}", on_click=place_bets)
            with c8:
                st.write("")
            with c9:
                st.write("")

        for game in game_options:
            df2 = df1[df1['game']==game]
            counter = df1[df1['game']==game].index.values[0]
            with st.container():
                st.write('---')
                #st.subheader(df2.game[counter])
                with st.container():
                    c1, c2, c3,c4, c5, c6, c7, c8, c9 = st.columns(9, gap="medium")
                    with c1:
                        st.markdown("*:black[Home Team]*")
                    with c2:
                        st.markdown(f"{df2.home_team[counter]}")
                    with c3:
                        st.button(
                            f"{df2.home_ml_odds[counter]}", 
                            key=f"{sportsbook}_{df2.home_team[counter]}_ml_{counter}", 
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.home_team[counter],"ML",df2.home_ml_odds[counter], )
                        )
                    with c4:
                        st.button(
                            f"{df2.home_spread[counter]}    {df2.home_spread_odds[counter]}", 
                            key=f"{sportsbook}_{df2.home_team[counter]}_s_{counter}",
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.home_team[counter],"Spread",df2.home_spread_odds[counter], )
                        )
                    with c5:
                        st.button(
                            f"O: {df2.home_total[counter]}    {df2.over_odds[counter]}", 
                            key=f"{sportsbook}_{df2.home_team[counter]}_t_{counter}",
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.home_team[counter],"Total",df2.over_odds[counter], )
                        )
                    with c6:
                        for bet in st.session_state.user_bets:
                            if (bet.game  == df2.game[counter] and bet.sportsbook == sportsbook and bet.team == df2.home_team[counter]):
                                st.code(bet.bet_type)
                    with c7:
                        for bet in st.session_state.user_bets:
                            if (bet.game  == df2.game[counter] and bet.sportsbook == sportsbook and bet.team == df2.home_team[counter]):
                                st.number_input("amount",key=f"bet_amount_{bet}", label_visibility="collapsed")
                    with c8:
                        for bet in st.session_state.user_bets:
                            if (bet.game  == df2.game[counter] and bet.sportsbook == sportsbook and bet.team == df2.home_team[counter]):
                                st.code(f"Payout : {round(payout(st.session_state[f'bet_amount_{bet}'],bet.odds),2)}")
                                
                with st.container():
                    c1, c2, c3,c4, c5, c6, c7, c8, c9= st.columns(9, gap="medium")
                    with c1:
                        st.markdown("*:red[Away Team]*")
                    with c2:
                        st.markdown(f"{df2.away_team[counter]}")
                    with c3:
                        st.button(
                            f"{df2.away_ml_odds[counter]}", 
                            key=f"{sportsbook}_{df2.away_team[counter]}_ml_{counter}",
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.away_team[counter],"ML",df2.away_ml_odds[counter], )
                        )

                    with c4:
                        st.button(
                            f"{df2.away_spread[counter]}    {df2.away_spread_odds[counter]}", 
                            key=f"{sportsbook}_{df2.away_team[counter]}_s_{counter}",
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.away_team[counter],"Spread",df2.away_spread_odds[counter], )
                        )
                    with c5:
                        st.button(
                            f"U: {df2.away_total[counter]}    {df2.under_odds[counter]}", 
                            key=f"{sportsbook}_{df2.away_team[counter]}_t_{counter}",
                            on_click=add_bet, 
                            args=(sportsbook,df2.game[counter],df2.away_team[counter],"Total",df2.under_odds[counter], )
                        )
                    with c6:
                        for bet in st.session_state.user_bets:
                            if (bet.game  == df2.game[counter] and bet.sportsbook == sportsbook and bet.team == df2.away_team[counter]):
                                st.code(bet.bet_type)
                    with c7:
                        for bet in st.session_state.user_bets:
                            if (bet.game  == df2.game[counter] and bet.sportsbook == sportsbook and bet.team == df2.away_team[counter]):
                                st.number_input("amount",key=f"bet_amount_{bet}", label_visibility="collapsed")
                    with c8:
                        for bet in st.session_state.user_bets:
                            if (bet.game  == df2.game[counter] and bet.sportsbook == sportsbook and bet.team == df2.away_team[counter]):
                                st.code(f"Payout : {round(payout(st.session_state[f'bet_amount_{bet}'],bet.odds),2)}")

    
