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
special_events = ["Superbowl 2023"]

# Filter for teams
options = st.multiselect(
    '**Select your event(s):**',
    options=special_events,
    default=special_events,
    key='Special Events'
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