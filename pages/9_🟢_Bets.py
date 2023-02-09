import streamlit as st
import pandas as pd
from Utils.tools import get_db_engine, initiate_database_tables, create_bet, retrieve_user_bets, nav_page, get_bet_id_counter, update_bet_status_payout, nav_page
from sqlalchemy import inspect
from Utils.Dictionaries import team_index_current
import re
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import asyncio
        
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

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#ensures a user is logged in (has address to transact)   
if 'user_account_addr' not in st.session_state or st.session_state['user_account_addr'] == "":
    st.session_state['user_account_addr'] = ""
    st.warning("User has not registered or logged in. Please do so before you start betting", icon="⚠️")
    nav_page("Account")

def render_page(db_engine,user_account_addr):
    
    WEI_FACTOR = 10**18
    SCORE_SCALING=100
    
    if 'user_account_addr' not in st.session_state or st.session_state['user_account_addr'] == "":
        st.session_state['user_account_addr'] = user_account_addr
        
    ##performs a contract call and Gets/stores users ethereum and cbet token balance, then stores in in escrow. 
    st.session_state.user_balance_wallet_ether = w3.eth.getBalance(st.session_state.user_account_addr)
    st.session_state.user_balance_wallet_token = contract.functions.balanceCbetTokens(st.session_state.user_account_addr).call()
    (st.session_state.user_balance_betting_ether, st.session_state.user_balance_betting_token) = contract.functions.getBalanceUserBetting(st.session_state.user_account_addr).call()
    (st.session_state.user_balance_escrow_ether, st.session_state.user_balance_escrow_token) = contract.functions.getBalanceUserEscrow(st.session_state.user_account_addr).call()

    ##Creates a container that is expandable and populates it with the users betting balances and also shows wei values
    with st.expander("User account balances", expanded=True):
        c1, c2, c3, c4 = st.columns([2,2,2,2])
        with c1:
            st.info('**User Wallet Balance Ether**')
            st.info('**User Betting Balance Ether**')
        with c2:
            st.info(format(st.session_state.user_balance_wallet_ether/WEI_FACTOR,'.6f'))
            st.info(format(st.session_state.user_balance_betting_ether/WEI_FACTOR,'.6f'))
        with c3:
            st.info('**User Wallet Balance token**')
            st.info('**User Betting Balance token**')
        with c4:
            st.info(format(st.session_state.user_balance_wallet_token/WEI_FACTOR,'.6f'))
            st.info(format(st.session_state.user_balance_betting_token/WEI_FACTOR,'.6f'))

    insp = inspect(db_engine)

    # Check if bet table already exists; if not, create one
    if len(insp.get_table_names()) == 0:
        initiate_database_tables(db_engine)

    #stores user bets in a variable during user session   
    bets = retrieve_user_bets(st.session_state.user_account_addr, db_engine)

    bets_ml = bets['ML']
    bets_spread = bets['Spread']
    bets_total = bets['Total']




    ##redners bets (one for each: ML, Spreads, Totals)

    with st.expander("🟢 MoneyLine Bets placed", expanded=True):
        with st.container():
            c1,c2,c3,c4,c5,c6,c7,c8 = st.columns([1,3.7,2,1,1.2,1,1,1])
            with c1:
                st.success('ID')
            with c2:
                st.success('Sportsbook | Game')
            with c3:
                st.success('Team')
            with c4:
                st.success('Odds')
            with c5:
                st.success('Amount')
            with c6:
                st.success('Ξ/🎲')
            with c7:
                st.success('Status')
            with c8:
                st.success('Payout')
            st.write("---")
        for bet in bets_ml:
            c1,c2,c3,c4,c5,c6,c7,c8 = st.columns([1,3.7,2,1,1.2,1,1,1])
            with c1:
                st.info(bet[0])
            with c2:
                st.info(f"{bet[1]} | {bet[2]}")
            with c3:
                st.info(bet[3])
            with c4:
                st.info(bet[5])
            with c5:
                st.info(bet[6]/WEI_FACTOR)
            with c6:
                if bet[10] == 1:
                    st.info("Ξ")
                else:
                    st.info("🎲")
            with c7:
                st.info(bet[11])
            with c8:
                if bet[12] ==  None:
                    st.info(bet[12])
                else:
                    st.info(format(bet[12]/WEI_FACTOR,'.6f'))

    with st.expander("🟢 Spread Bets placed"):
        with st.container():
            c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([1,3.7,1.8,1,1.2,1,0.8,1,1])
            with c1:
                st.success('Bet ID')
            with c2:
                st.success('Sportsbook | Game')
            with c3:
                st.success('Team')
            with c4:
                st.success('Odds')
            with c5:
                st.success('Spread')
            with c6:
                st.success('Amount')
            with c7:
                st.success('Ξ/🎲')
            with c8:
                st.success('Status')
            with c9:
                st.success('Payout')
            st.write("---")

        for bet in bets_spread:
            c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([1,3.7,1.8,1,1.2,1,0.8,1,1])
            with c1:
                st.info(bet[0])
            with c2:
                st.info(f"{bet[1]} | {bet[2]}")
            with c3:
                st.info(bet[3])
            with c4:
                st.info(bet[5])
            with c5:
                st.info(bet[7])
            with c6:
                st.info(bet[6]/WEI_FACTOR)
            with c7:
                if bet[10] == 1:
                    st.info("Ξ")
                else:
                    st.info("🎲")
            with c8:
                st.info(bet[11]) 
            with c9:
                if bet[12] ==  None:
                    st.info(bet[12])
                else:
                    st.info(format(bet[12]/WEI_FACTOR,'.6f'))

    with st.expander("🟢 Total (Under/Over) Bets placed"):
        with st.container():
            c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([1,3.7,1.8,1,1.2,1,0.8,1,1])
            with c1:
                st.success('Bet ID')
            with c2:
                st.success('Sportsbook | Game')
            with c3:
                st.success('Team')
            with c4:
                st.success('Odds')
            with c5:
                st.success('U/O | Total')
            with c6:
                st.success('Amount')
            with c7:
                st.success('Ξ/🎲')
            with c8:
                st.success('Status')
            with c9:
                st.success('Payout')
            st.write("---")

        for bet in bets_total:
            c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([1,3.7,1.8,1,1.2,1,0.8,1,1])
            with c1:
                st.info(bet[0])
            with c2:
                st.info(f"{bet[1]} | {bet[2]}")
            with c3:
                st.info(bet[3])
            with c4:
                st.info(bet[5])
            with c5:
                if bet[9] == 1:
                    st.info(f"O | {bet[8]/SCORE_SCALING}")
                else:
                    st.info(f"U | {bet[8]/SCORE_SCALING}")
            with c6:
                st.info(bet[6]/WEI_FACTOR)
            with c7:
                if bet[10] == 1:
                    st.info("Ξ")
                else:
                    st.info("🎲")
            with c8:
                st.info(bet[11])
            with c9:
                if bet[12] ==  None:
                    st.info(bet[12])
                else:
                    st.info(format(bet[12]/WEI_FACTOR,'.6f'))

    # define function to handle events
def handle_event(event,db_engine,user_account_addr):
    x = json.loads(Web3.toJSON(event))
    bet_info = x['args']
    update_bet_status_payout(bet_info['_betId'], bet_info['_payout'],"Settled",db_engine)
    #render_page(db_engine,user_account_addr)
    raise Exception('Stop this thing')
    #(bet_id, payout, status, db_engine)
    


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "gameEventPayout" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval,db_engine,user_account_addr):
    while True:
        for gameEventPayout in event_filter.get_new_entries():
            handle_event(gameEventPayout,db_engine,user_account_addr)
        await asyncio.sleep(poll_interval)
    #nav_page("Bets")


# when main is called
# create a filter for the latest block and look for the "gameEventPayout" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 3 seconds
def main():
    # get database engine
    db_engine = get_db_engine()
    user_account_addr = st.session_state['user_account_addr']
    render_page(db_engine,user_account_addr)
    
    event_filter = contract.events.gameEventPayout.createFilter(fromBlock='latest')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 3,db_engine, user_account_addr)))
    except Exception as ex:
        loop.close()
        st.experimental_rerun()
    finally:
        # close loop to free up system resources
        loop.close()
    

if __name__ == "__main__":
    main()