import streamlit as st
import pandas as pd
from Utils.tools import get_db_engine, initiate_database_tables, create_bet, retrieve_user_bets, nav_page, get_bet_id_counter
        
        
# Layout
st.set_page_config(page_title='Bets placed by User', page_icon=':bar_chart:', layout='wide')
st.title('🟢 Your bets')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
if 'user_account_addr' not in st.session_state or st.session_state['user_account_addr'] == "":
    st.session_state['user_account_addr'] = ""
    st.warning("User has not registered or logged in. Please do so before you start betting", icon="⚠️")
    nav_page("Account")

# get database engine
db_engine = get_db_engine()
        
# Check if bet table already exists; if not, create one
if len(db_engine.table_names()) == 0:
    initiate_database_tables(db_engine)
    
bets = retrieve_user_bets(st.session_state.user_account_addr, db_engine)

bets_ml = bets['ML']
bets_spread = bets['Spread']
bets_total = bets['Total']

WEI_FACTOR = 10**18
SCORE_SCALING=100

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
            if bet[11] == 'None':
                st.info("Pending")
            else:
                st.info("Settled")
        with c8:
            st.info(bet[12])

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
            if bet[11] == 'None':
                st.info("Pending")
            else:
                st.info("Settled")
        with c9:
            st.info(bet[12])
            
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
            st.info(bet[10])
        with c8:
            st.info(bet[11])
        with c9:
            st.info(bet[12])