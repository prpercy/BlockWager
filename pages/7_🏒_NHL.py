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
nhl_teams = [
    "Anaheim Ducks",    "Arizona Coyotes",    "Boston Bruins",    "Buffalo Sabres",
    "Calgary Flames",    "Carolina Hurricanes",    "Chicago Blackhawks",    "Colorado Avalanche",
    "Columbus Blue Jackets",    "Dallas Stars",    "Detroit Red Wings",    "Edmonton Oilers",
    "Florida Panthers",    "Los Angeles Kings",    "Minnesota Wild",    "Montreal Canadiens",
    "Nashville Predators",    "New Jersey Devils",    "New York Islanders",    "New York Rangers",
    "Ottawa Senators",    "Philadelphia Flyers",    "Pittsburgh Penguins",    "San Jose Sharks",
    "St. Louis Blues",    "Tampa Bay Lightning",    "Toronto Maple Leafs",    "Vancouver Canucks",
    "Vegas Golden Knights",    "Washington Capitals",    "Winnipeg Jets"]


# Filter for teams
options = st.multiselect(
    '**Select your team(s):**',
    options=nhl_teams,
    default=nhl_teams,
    key='NHL Teams'
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