# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

# Layout
st.set_page_config(page_title='[Under construction]', page_icon='🚧', layout='wide')
st.title('🚧 [Page Under construction]')


#Sportsbooks list
sportsbooks = ['fanduel', 'draftkings', 'betmgm', 'pointsbet', 'caesars', 'wynn', 'bet_rivers_ny']

# Filter for sportsbooks
options = st.multiselect(
    '**Select your sportsbook(s):**',
    options=sportsbooks,
    default=sportsbooks,
    key='Sportsbooks'
)

#Team list
nfl_teams = [    "Arizona Cardinals",    "Atlanta Falcons",    "Baltimore Ravens",    "Buffalo Bills",    
"Carolina Panthers",    "Chicago Bears",    "Cincinnati Bengals",    "Cleveland Browns",    "Dallas Cowboys",    
"Denver Broncos",    "Detroit Lions",    "Green Bay Packers",    "Houston Texans",    "Indianapolis Colts",    
"Jacksonville Jaguars",    "Kansas City Chiefs",    "Las Vegas Raiders",    "Los Angeles Chargers",    
"Los Angeles Rams",    "Miami Dolphins",    "Minnesota Vikings",    "New England Patriots",    "New Orleans Saints",    
"New York Giants",    "New York Jets",    "Philadelphia Eagles",    "Pittsburgh Steelers",    "San Francisco 49ers",    
"Seattle Seahawks",    "Tampa Bay Buccaneers",    "Tennessee Titans",    "Washington Football Team"]


# Filter for teams
options = st.multiselect(
    '**Select your team(s):**',
    options=nfl_teams,
    default=nfl_teams,
    key='NFL Teams'
)

tab1, tab2, tab3 = st.tabs(["Spread", "Money", "Total"])

with tab1:
   st.subheader("Odds")
#Odds and betting code to be inserted here

with tab2:
    st.subheader("Odds")
#Odds and betting code to be inserted here

with tab3:
   st.subheader("Odds")
#Odds and betting code to be inserted here