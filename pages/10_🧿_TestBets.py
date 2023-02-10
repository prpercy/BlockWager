import streamlit as st
import pandas as pd
from Utils.tools import get_db_engine, initiate_database_tables, create_bet, retrieve_user_bets, nav_page, get_bet_id_counter, update_bet_status_payout
from sqlalchemy import inspect
from Utils.Dictionaries import team_index_current
import re
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv

        
# Layout
st.set_page_config(page_title='Bets placed by User', page_icon=':bar_chart:', layout='wide')
st.title('🟢 Your bets')

# environment Variables
load_dotenv("./blockwager.env")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/cbet_abi.json')) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    
    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

contract = load_contract()

##logic that determines if a bet is a winner or loser for totals
def win_lose_total_bet(bet_id, winning_team_id, is_over_int, total):
    if is_over_int == 1:
        # winning_score + losing_score > total
        losing_score = int(total*0.3)
        winning_score= int(total - losing_score+total*0.5)
    else:
        # winning_score + losing_score < total
        losing_score = int(total*0.3)
        winning_score= int(total - losing_score - total*0.1)
    contract.functions.gameEvent(bet_id, winning_team_id, winning_score, losing_score).transact({'from': st.session_state.cbet_account_betting_addr, 'gas': 1000000})
    
##logic that determines if a bet is a winner or loser for spreads
def win_lose_spread_bet(bet_id, winning_team_id, spread):
    losing_score = 100
    winning_score=int(losing_score+spread+50)
    contract.functions.gameEvent(bet_id, winning_team_id, winning_score, losing_score).transact({'from': st.session_state.cbet_account_betting_addr, 'gas': 1000000})

def win_lose_ml_bet(bet_id, winning_team_id):
    losing_score = 100
    winning_score=losing_score+10
    contract.functions.gameEvent(bet_id, winning_team_id, winning_score, losing_score).transact({'from': st.session_state.cbet_account_betting_addr, 'gas': 1000000})

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
 #ensures a user is logged in (has address to transact)   
if 'user_account_addr' not in st.session_state or st.session_state['user_account_addr'] == "":
    st.session_state['user_account_addr'] = ""
    st.warning("User has not registered or logged in. Please do so before you start betting", icon="⚠️")
    nav_page("Account")

# get database engine
db_engine = get_db_engine()
insp = inspect(db_engine)

# Check if bet table already exists; if not, create one
if len(insp.get_table_names()) == 0:
    initiate_database_tables(db_engine)
 #stores user bets in a variable during user session   
bets = retrieve_user_bets(st.session_state.user_account_addr, db_engine)

bets_ml = bets['ML']
bets_spread = bets['Spread']
bets_total = bets['Total']

WEI_FACTOR = 10**18
SCORE_SCALING=100
    

with st.container():
    c1,c2,c3,c4,c5 = st.columns([1,4,2,1,1])
    with c1:
        st.success('ID')
    with c2:
        st.success('Sportsbook | Game')
    with c3:
        st.success('Team')
    with c4:
        st.success('Win')
    with c5:
        st.success('Lose')
    st.write("---")

with st.expander("🟢 Money Line Bets", expanded=True):
    for bet in bets_ml:
        if bet[11] != "Settled":
            c1,c2,c3,c4,c5 = st.columns([1,4,2,1,1])
            with c1:
                st.info(bet[0])
            with c2:
                st.info(f"{bet[1]} | {bet[2]}")
            with c3:
                st.info(bet[3])
            with c4:
                st.button(
                    "Win", 
                    key=f"{bet[0]}_Win", 
                    on_click=win_lose_ml_bet, 
                    args=(bet[0],team_index_current[bet[3]], )
                    #args=(betID, teamID, )
                )
            with c5:
                st.button(
                    "Lose", 
                    key=f"{bet[0]}_Lose", 
                    on_click=win_lose_ml_bet, 
                    args=(bet[0],team_index_current[bet[3]]+1, )
                    #args=(betID, teamID,)
                )

with st.expander("🟢 Spread Bets", expanded=True):
    for bet in bets_spread:
        if bet[11] != "Settled":
            c1,c2,c3,c4,c5 = st.columns([1,4,2,1,1])
            with c1:
                st.info(bet[0])
            with c2:
                st.info(f"{bet[1]} | {bet[2]}")
            with c3:
                st.info(bet[3])
            with c4:
                st.button(
                    "Win", 
                    key=f"{bet[0]}_Win", 
                    on_click=win_lose_spread_bet, 
                    args=(bet[0],team_index_current[bet[3]],bet[7] )
                    #args=(betID, teamID, spread,)
                )
            with c5:
                st.button(
                    "Lose", 
                    key=f"{bet[0]}_Lose", 
                    on_click=win_lose_spread_bet, 
                    args=(bet[0],team_index_current[bet[3]]+1,bet[7] )
                    #args=(betID, teamID, spread,)
                )

with st.expander("🟢 Total Over/Under Bets", expanded=True):
    for bet in bets_total:
        if bet[11] != "Settled":
            c1,c2,c3,c4,c5 = st.columns([1,4,2,1,1])
            with c1:
                st.info(bet[0])
            with c2:
                st.info(f"{bet[1]} | {bet[2]}")
            with c3:
                st.info(bet[3])
            with c4:
                st.button(
                    "Win", 
                    key=f"{bet[0]}_Win", 
                    on_click=win_lose_total_bet, 
                    args=(bet[0],team_index_current[bet[3]], bet[9], bet[8]/SCORE_SCALING,)
                    #args=(betID, teamID, isOver, total)

                )
            with c5:
                st.button(
                    "Lose", 
                    key=f"{bet[0]}_Lose", 
                    on_click=win_lose_total_bet, 
                    args=(bet[0],team_index_current[bet[3]]+1, bet[9], bet[8]/SCORE_SCALING,)
                    #args=(betID, teamID, isOver, total)
                )

