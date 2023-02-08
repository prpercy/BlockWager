# Libraries
import streamlit as st
import pandas as pd
import argparse
from colorama import Fore, Style
from Utils.tools import get_json_data, to_data_frame, payout
from Utils.Dictionaries import team_index_current, sportsbook_index
from OddsProvider.SbrOddsProvider import SbrOddsProvider
import os 
import json 
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv

# Layout
st.set_page_config(page_title='[Under construction]', page_icon='🚧', layout='wide')
st.title('🚧 [Page Under construction]')


# if 'user_account_addr' not in st.session_state:
#     st.session_state['user_account_addr'] = ''
# st.caption(f'ACCOUNT: {st.session_state.user_account_addr}!!!')
# st.caption(f"Cbet account {st.session_state.cbet_account_owner_addr}!!!")
# WEI_FACTOR = 10**18 
# load_dotenv('./blockwagwer.env')

# w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


# @st.cache(allow_output_mutation=True)
# contract = 5_🏀_NBA.load_contract()
# #Sportsbooks list
# sportsbooks = ['fanduel', 'draftkings', 'betmgm', 'pointsbet', 'caesars', 'wynn', 'bet_rivers_ny']

# # Filter for sportsbooks
# options = st.multiselect(
#     '**Select your sportsbook(s):**',
#     options=sportsbooks,
#     default=sportsbooks,
#     key='Sportsbooks'
# )
# todays_games_url = ''
# data_url= ''

# #Team list
# nhl_teams = [
#     "Anaheim Ducks",    "Arizona Coyotes",    "Boston Bruins",    "Buffalo Sabres",
#     "Calgary Flames",    "Carolina Hurricanes",    "Chicago Blackhawks",    "Colorado Avalanche",
#     "Columbus Blue Jackets",    "Dallas Stars",    "Detroit Red Wings",    "Edmonton Oilers",
#     "Florida Panthers",    "Los Angeles Kings",    "Minnesota Wild",    "Montreal Canadiens",
#     "Nashville Predators",    "New Jersey Devils",    "New York Islanders",    "New York Rangers",
#     "Ottawa Senators",    "Philadelphia Flyers",    "Pittsburgh Penguins",    "San Jose Sharks",
#     "St. Louis Blues",    "Tampa Bay Lightning",    "Toronto Maple Leafs",    "Vancouver Canucks",
#     "Vegas Golden Knights",    "Washington Capitals",    "Winnipeg Jets"]


# # Filter for teams
# options = st.multiselect(
#     '**Select your team(s):**',
#     options=nhl_teams,
#     default=nhl_teams,
#     key='NHL Teams'
# )
