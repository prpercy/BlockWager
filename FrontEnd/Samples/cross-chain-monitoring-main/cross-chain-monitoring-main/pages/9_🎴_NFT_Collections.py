# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Global Variables
theme_plotly = None # None or streamlit
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Layout
st.set_page_config(page_title='NFT Collections - Cross Chain Monitoring', page_icon=':bar_chart:', layout='wide')
st.title('🎴 NFT Collections')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Google Analytics
st.components.v1.html("""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-PQ45JJR2R7"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-PQ45JJR2R7');
    </script>
""", height=1, scrolling=False)

# Data Sources
@st.cache(ttl=600)
def get_data(query):
    if query == 'NFTs Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/a9dee9b9-bfd8-4fed-b49b-a03767306d89/data/latest')
    elif query == 'NFTs Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/6ec4aca1-3d25-4233-bec2-0443b27d3e6c/data/latest')
    elif query == 'NFTs Heatmap':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/62fa2182-ca1b-4648-a363-8d1ce591253e/data/latest')
    elif query == 'NFTs Marketplaces Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/8f4e8520-52af-4d57-b29e-e513f62f8fa9/data/latest')
    elif query == 'NFTs Marketplaces Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/8fcca211-4bc6-444d-8696-0a583e2966a6/data/latest')
    elif query == 'NFTs Collections Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/eaa5902c-0206-4fd7-8eb4-b15ecf9a71b4/data/latest')
    elif query == 'NFTs Collections Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/3cb9e6f6-849b-47e6-8c7e-b454e1394d6b/data/latest')
    return None

nfts_collections_overview = get_data('NFTs Collections Overview')
nfts_collections_daily = get_data('NFTs Collections Daily')

# Filter the blockchains
options = st.multiselect(
    '**Select your desired blockchains:**',
    options=nfts_collections_overview['Blockchain'].unique(),
    default=nfts_collections_overview['Blockchain'].unique(),
    key='collections_options'
)

# Selected Blockchain
if len(options) == 0:
    st.warning('Please select at least one blockchain to see the metrics.')

# Single chain Analysis
elif len(options) == 1:
    subtab_overview, subtab_prices = st.tabs(['Overview', 'Prices'])

    with subtab_overview:
        st.subheader('Overview')
        df = nfts_collections_overview.query('Blockchain == @options')
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(df.sort_values('Volume', ascending=False).head(30), x='Collection', y='Volume', color='Collection', title='Total Sales Volume', log_y=True)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Volume [USD]')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.bar(df.sort_values('Buyers', ascending=False).head(30), x='Collection', y='Buyers', color='Collection', title='Total Buyers', log_y=True)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Buyers')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        with c2:
            fig = px.bar(df.sort_values('Sales', ascending=False).head(30), x='Collection', y='Sales', color='Collection', title='Total Sales', log_y=True)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Sales')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.bar(df.sort_values('NFTs', ascending=False).head(30), x='Collection', y='NFTs', color='Collection', title='Total Traded NFTs', log_y=True)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='NFTs')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        st.subheader('Market Shares')
        c1, c2 = st.columns(2)
        with c1:
            df = nfts_collections_overview.query('Blockchain == @options')
            df = df.groupby(['Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
            df['RowNumber'] = df['Volume'].rank(method='max', ascending=False)
            df.loc[df['RowNumber'] > 10, 'Collection'] = 'Other'
            fig = px.pie(df, values='Volume', names='Collection', title='Share of Total Sales Volume')
            fig.update_layout(legend_title=None, legend_y=0.5)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            df = nfts_collections_overview.query('Blockchain == @options')
            df = df.groupby(['Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
            df['RowNumber'] = df['Buyers'].rank(method='max', ascending=False)
            df.loc[df['RowNumber'] > 10, 'Collection'] = 'Other'
            fig = px.pie(df, values='Volume', names='Collection', title='Share of Total Buyers')
            fig.update_layout(legend_title=None, legend_y=0.5)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        with c2:
            df = nfts_collections_overview.query('Blockchain == @options')
            df = df.groupby(['Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
            df['RowNumber'] = df['Sales'].rank(method='max', ascending=False)
            df.loc[df['RowNumber'] > 10, 'Collection'] = 'Other'
            fig = px.pie(df, values='Sales', names='Collection', title='Share of Total Sales')
            fig.update_layout(legend_title=None, legend_y=0.5)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            df = nfts_collections_overview.query('Blockchain == @options')
            df = df.groupby(['Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
            df['RowNumber'] = df['NFTs'].rank(method='max', ascending=False)
            df.loc[df['RowNumber'] > 10, 'Collection'] = 'Other'
            fig = px.pie(df, values='Volume', names='Collection', title='Share of Total Traded NFTs')
            fig.update_layout(legend_title=None, legend_y=0.5)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        st.subheader('Activity Over Time')

        df = nfts_collections_daily.query('Blockchain == @options')
        df = df.groupby(['Date', 'Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby(['Date'])['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Collection'] = 'Other'
        df = df.groupby(['Date', 'Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()

        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='Volume', color='Collection', title='Daily Sales Volume of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.bar(df.sort_values(['Date', 'Sales'], ascending=[True, False]), x='Date', y='Sales', color='Collection', title='Daily Sales of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Sales')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = px.bar(df.sort_values(['Date', 'Buyers'], ascending=[True, False]), x='Date', y='Buyers', color='Collection', title='Daily Buyers of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Buyers')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = px.bar(df.sort_values(['Date', 'NFTs'], ascending=[True, False]), x='Date', y='NFTs', color='Collection', title='Daily Traded NFTs of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='NFTs')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
           
        with c2:
            fig = go.Figure()
            for i in df['Collection'].unique():
                fig.add_trace(go.Scatter(
                    name=i,
                    x=df.query("Collection == @i")['Date'],
                    y=df.query("Collection == @i")['Volume'],
                    mode='lines',
                    stackgroup='one',
                    groupnorm='percent'
                ))
            fig.update_layout(title='Daily Share of Sales Volume of Top Collections By Volume')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = go.Figure()
            for i in df['Collection'].unique():
                fig.add_trace(go.Scatter(
                    name=i,
                    x=df.query("Collection == @i")['Date'],
                    y=df.query("Collection == @i")['Sales'],
                    mode='lines',
                    stackgroup='one',
                    groupnorm='percent'
                ))
            fig.update_layout(title='Daily Share of Sales of Top Collections By Volume')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = go.Figure()
            for i in df['Collection'].unique():
                fig.add_trace(go.Scatter(
                    name=i,
                    x=df.query("Collection == @i")['Date'],
                    y=df.query("Collection == @i")['Buyers'],
                    mode='lines',
                    stackgroup='one',
                    groupnorm='percent'
                ))
            fig.update_layout(title='Daily Share of Buyers of Top Collections By Volume')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = go.Figure()
            for i in df['Collection'].unique():
                fig.add_trace(go.Scatter(
                    name=i,
                    x=df.query("Collection == @i")['Date'],
                    y=df.query("Collection == @i")['NFTs'],
                    mode='lines',
                    stackgroup='one',
                    groupnorm='percent'
                ))
            fig.update_layout(title='Daily Share of Traded NFTs of Top Collections By Volume')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    with subtab_prices:
        st.subheader('Overview')
        df = nfts_collections_overview.query('Blockchain == @options')
        
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(df.sort_values('PriceAverage', ascending=False).head(30), x='Collection', y='PriceAverage', color='Collection', title='Average Price of NFT Collections', log_y=True)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Average [USD]')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.bar(df.sort_values('PriceMax', ascending=False).head(30), x='Collection', y='PriceMax', color='Collection', title='Maximum Price of NFT Collections', log_y=True)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Maximum [USD]')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        with c2:
            fig = px.bar(df.sort_values('PriceMedian', ascending=False).head(30), x='Collection', y='PriceMedian', color='Collection', title='Median Price of NFT Collections', log_y=True)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Median [USD]')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.bar(df.sort_values('PriceFloor', ascending=False).head(30), x='Collection', y='PriceFloor', color='Collection', title='Floor Price of NFT Collections', log_y=True)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Floor [USD]')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        st.subheader('Activity Over Time')

        df = nfts_collections_daily.query('Blockchain == @options')
        df = df.groupby(['Date', 'Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby(['Date'])['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Collection'] = 'Other'
        df = df.groupby(['Date', 'Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()

        c1, c2 = st.columns(2)
        with c1:
            fig = px.line(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='PriceAverage', color='Collection', title='Daily Average Price of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = px.line(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='PriceMax', color='Collection', title='Daily Maximum Price of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        with c2:
            fig = px.line(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='PriceMedian', color='Collection', title='Daily Median Price of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = px.line(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='PriceFloor', color='Collection', title='Daily Floor Price of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

# Cross Chain Comparison
else:
    subtab_overview, subtab_prices = st.tabs(['Overview', 'Prices'])

    with subtab_overview:
        st.subheader('Overview')
        df = nfts_collections_overview.query('Blockchain == @options')
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(df.sort_values('Volume', ascending=False).head(30), x='Collection', y='Volume', color='Blockchain', title='Total Sales Volume of Top NFT Collections', log_y=True)
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.bar(df.sort_values('Buyers', ascending=False).head(30), x='Collection', y='Buyers', color='Blockchain', title='Total Buyers of Top NFT Collections', log_y=True)
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Buyers')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        with c2:
            fig = px.bar(df.sort_values('Sales', ascending=False).head(30), x='Collection', y='Sales', color='Blockchain', title='Total Sales of Top NFT Collections', log_y=True)
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Sales')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.bar(df.sort_values('NFTs', ascending=False).head(30), x='Collection', y='NFTs', color='Blockchain', title='Total Traded NFTs of Top NFT Collections', log_y=True)
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='NFTs')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        st.subheader('Market Shares')
        c1, c2 = st.columns(2)
        with c1:
            df = nfts_collections_overview.query('Blockchain == @options')
            df = df.groupby(['Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
            df['RowNumber'] = df['Volume'].rank(method='max', ascending=False)
            df.loc[df['RowNumber'] > 10, 'Collection'] = 'Other'
            fig = px.pie(df, values='Volume', names='Collection', title='Share of Total Sales Volume')
            fig.update_layout(legend_title=None, legend_y=0.5)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            df = nfts_collections_overview.query('Blockchain == @options')
            df = df.groupby(['Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
            df['RowNumber'] = df['Buyers'].rank(method='max', ascending=False)
            df.loc[df['RowNumber'] > 10, 'Collection'] = 'Other'
            fig = px.pie(df, values='Volume', names='Collection', title='Share of Total Buyers')
            fig.update_layout(legend_title=None, legend_y=0.5)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        with c2:
            df = nfts_collections_overview.query('Blockchain == @options')
            df = df.groupby(['Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
            df['RowNumber'] = df['Sales'].rank(method='max', ascending=False)
            df.loc[df['RowNumber'] > 10, 'Collection'] = 'Other'
            fig = px.pie(df, values='Sales', names='Collection', title='Share of Total Sales')
            fig.update_layout(legend_title=None, legend_y=0.5)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            df = nfts_collections_overview.query('Blockchain == @options')
            df = df.groupby(['Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
            df['RowNumber'] = df['NFTs'].rank(method='max', ascending=False)
            df.loc[df['RowNumber'] > 10, 'Collection'] = 'Other'
            fig = px.pie(df, values='Volume', names='Collection', title='Share of Total Traded NFTs')
            fig.update_layout(legend_title=None, legend_y=0.5)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        st.subheader('Activity Over Time')

        df = nfts_collections_daily.query('Blockchain == @options')
        df = df.groupby(['Date', 'Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby(['Date'])['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Collection'] = 'Other'
        df = df.groupby(['Date', 'Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()

        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='Volume', color='Collection', title='Daily Sales Volume of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.bar(df.sort_values(['Date', 'Sales'], ascending=[True, False]), x='Date', y='Sales', color='Collection', title='Daily Sales of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Sales')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = px.bar(df.sort_values(['Date', 'Buyers'], ascending=[True, False]), x='Date', y='Buyers', color='Collection', title='Daily Buyers of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Buyers')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = px.bar(df.sort_values(['Date', 'NFTs'], ascending=[True, False]), x='Date', y='NFTs', color='Collection', title='Daily Traded NFTs of Top Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='NFTs')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
           
        with c2:
            fig = go.Figure()
            for i in df['Collection'].unique():
                fig.add_trace(go.Scatter(
                    name=i,
                    x=df.query("Collection == @i")['Date'],
                    y=df.query("Collection == @i")['Volume'],
                    mode='lines',
                    stackgroup='one',
                    groupnorm='percent'
                ))
            fig.update_layout(title='Daily Share of Sales Volume of Top Collections By Volume')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = go.Figure()
            for i in df['Collection'].unique():
                fig.add_trace(go.Scatter(
                    name=i,
                    x=df.query("Collection == @i")['Date'],
                    y=df.query("Collection == @i")['Sales'],
                    mode='lines',
                    stackgroup='one',
                    groupnorm='percent'
                ))
            fig.update_layout(title='Daily Share of Sales of Top Collections By Volume')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = go.Figure()
            for i in df['Collection'].unique():
                fig.add_trace(go.Scatter(
                    name=i,
                    x=df.query("Collection == @i")['Date'],
                    y=df.query("Collection == @i")['Buyers'],
                    mode='lines',
                    stackgroup='one',
                    groupnorm='percent'
                ))
            fig.update_layout(title='Daily Share of Buyers of Top Collections By Volume')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
            
            fig = go.Figure()
            for i in df['Collection'].unique():
                fig.add_trace(go.Scatter(
                    name=i,
                    x=df.query("Collection == @i")['Date'],
                    y=df.query("Collection == @i")['NFTs'],
                    mode='lines',
                    stackgroup='one',
                    groupnorm='percent'
                ))
            fig.update_layout(title='Daily Share of Traded NFTs of Top Collections By Volume')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    with subtab_prices:
        st.subheader('Overview')
        df = nfts_collections_overview.query('Blockchain == @options')
        
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(df.sort_values('PriceAverage', ascending=False).head(30), x='Collection', y='PriceAverage', color='Blockchain', title='Average Price of Top NFT Collections', log_y=True)
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Average [USD]')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.bar(df.sort_values('PriceMax', ascending=False).head(30), x='Collection', y='PriceMax', color='Blockchain', title='Maximum Price of Top NFT Collections', log_y=True)
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Maximum [USD]')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        with c2:
            fig = px.bar(df.sort_values('PriceMedian', ascending=False).head(30), x='Collection', y='PriceMedian', color='Blockchain', title='Median Price of Top NFT Collections', log_y=True)
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Median [USD]')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.bar(df.sort_values('PriceFloor', ascending=False).head(30), x='Collection', y='PriceFloor', color='Blockchain', title='Floor Price of Top NFT Collections', log_y=True)
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Floor [USD]')
            fig.update_xaxes(type='category', categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        st.subheader('Activity Over Time')

        df = nfts_collections_daily.query('Blockchain == @options')
        df = df.groupby(['Date', 'Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby(['Date'])['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Collection'] = 'Other'
        df = df.groupby(['Date', 'Collection']).agg({'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()

        c1, c2 = st.columns(2)
        with c1:
            fig = px.line(df.sort_values(['Date', 'PriceAverage'], ascending=[True, False]), x='Date', y='PriceAverage', color='Collection', log_y=True, title='Daily Average Price of Top NFT Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Average Price [USD]')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.line(df.sort_values(['Date', 'PriceMax'], ascending=[True, False]), x='Date', y='PriceMax', color='Collection', log_y=True, title='Daily Maximum Price of Top NFT Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Maximum Price [USD]')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        with c2:
            fig = px.line(df.sort_values(['Date', 'PriceMedian'], ascending=[True, False]), x='Date', y='PriceMedian', color='Collection', log_y=True, title='Daily Median Price of Top NFT Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Median Price [USD]')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

            fig = px.line(df.sort_values(['Date', 'PriceFloor'], ascending=[True, False]), x='Date', y='PriceFloor', color='Collection', log_y=True, title='Daily Floor Price of Top NFT Collections By Volume')
            fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Floor Price [USD]')
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
