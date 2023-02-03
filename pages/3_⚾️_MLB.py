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
    '**Select your team(s):**',
    options=mlb_teams,
    default=mlb_teams,
    key='MLB Teams'
)

#Team list
mlb_teams = ["Arizona Diamondbacks",    "Atlanta Braves",    "Baltimore Orioles",    
"Boston Red Sox",    "Chicago Cubs",    "Chicago White Sox",    "Cincinnati Reds",    
"Cleveland Indians",    "Colorado Rockies",    "Detroit Tigers",    "Houston Astros",    
"Kansas City Royals",    "Los Angeles Angels",    "Los Angeles Dodgers",    "Miami Marlins",    
"Milwaukee Brewers",    "Minnesota Twins",    "New York Mets",    "New York Yankees",    "Oakland Athletics",    
"Philadelphia Phillies",    "Pittsburgh Pirates",    "San Diego Padres",    "San Francisco Giants",    "Seattle Mariners",    
"St. Louis Cardinals",    "Tampa Bay Rays",    "Texas Rangers",    "Toronto Blue Jays",    "Washington Nationals"]


# Filter for teams
options = st.multiselect(
    '**Select your team(s):**',
    options=mlb_teams,
    default=mlb_teams,
    key='MLB Teams'
)

tab1, tab2, tab3 = st.tabs(["Spread", "Money", "Total"])

with tab1:
   st.header("Odds")
#Odds and betting code to be inserted here

with tab2:
    st.header("Odds")
#Odds and betting code to be inserted here

with tab3:
   st.header("Odds")
#Odds and betting code to be inserted here