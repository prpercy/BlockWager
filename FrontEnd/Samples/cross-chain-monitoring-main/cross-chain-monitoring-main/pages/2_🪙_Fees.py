# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

# Global Variables
theme_plotly = None # None or streamlit
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Layout
st.set_page_config(page_title='Fees - Cross Chain Monitoring', page_icon=':bar_chart:', layout='wide')
st.title('🪙 Transaction Fees')

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
    if query == 'Transactions Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/579714e6-986e-421a-85dd-c32a8b41b25c/data/latest')
    elif query == 'Transactions Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/4e0c69ff-9395-43c1-af49-f590f864d339/data/latest')
    elif query == 'Transactions Heatmap':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/9d8d54d4-b700-4d85-af17-8c29aa29d334/data/latest')
    elif query == 'Transactions Fee Payers':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/7eae69ea-2387-420d-b4b9-6eceeb5ef22d/data/latest')
    return None

transactions_overview = get_data('Transactions Overview')
transactions_daily = get_data('Transactions Daily')
transactions_heatmap = get_data('Transactions Heatmap')
transactions_fee_payers = get_data('Transactions Fee Payers')

# Filter the blockchains
options = st.multiselect(
    '**Select your desired blockchains:**',
    options=transactions_overview['Blockchain'].unique(),
    default=transactions_overview['Blockchain'].unique(),
    key='fees_options'
)

# Selected Blockchain
if len(options) == 0:
    st.warning('Please select at least one blockchain to see the metrics.')

# Single chain Analysis
elif len(options) == 1:
    st.subheader('Overview')
    df = transactions_overview.query("Blockchain == @options")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Total Transaction Fees**', value=str(df['Fees'].map('{:,.0f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Average Fee Amount**', value=str(df['FeeAverage'].map('{:,.4f}'.format).values[0]), help='USD')
    with c3:
        st.metric(label='**Median Fee Amount**', value=str(df['FeeMedian'].map('{:,.4f}'.format).values[0]), help='USD')
    with c4:
        st.metric(label='**Average Fees/Block**', value=str(df['Fees/Block'].map('{:,.4f}'.format).values[0]), help='USD')
    
    st.subheader('Activity Over Time')
    df = transactions_daily.query("Blockchain == @options")

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['Date'], y=df['Fees'], name='Total Fees'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['Fees/Block'], name='Fees/Block'), secondary_y=True)
    fig.update_layout(title_text='Daily Total Transaction Fees and Average Fees/Block')
    fig.update_yaxes(title_text='Total Fees [USD]', secondary_y=False)
    fig.update_yaxes(title_text='Fees/Block [USD]', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['Date'], y=df['FeeAverage'], name='Average'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['FeeMedian'], name='Median'), secondary_y=True)
    fig.update_layout(title_text='Daily Average and Median Fee')
    fig.update_yaxes(title_text='Average [USD]', secondary_y=False)
    fig.update_yaxes(title_text='Median [USD]', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Heatmap')
    df = transactions_heatmap.query("Blockchain == @options")

    fig = px.density_heatmap(df, x='Hour', y='Day', z='Fees', histfunc='avg', title='Heatmap of Transaction Fees', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Fees [USD]'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.density_heatmap(df, x='Hour', y='Day', z='FeeAverage', histfunc='avg', title='Heatmap of Average Fee', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Average [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.density_heatmap(df, x='Hour', y='Day', z='FeeMedian', histfunc='avg', title='Heatmap of Median Fee', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Median [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Top Fee Payers')
    df = transactions_fee_payers.query("Blockchain == @options")
    fig = px.bar(df, x='User', y='Fees', color='User', title='Total Transaction Fees Paid By Top Fee Payers')
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Fees [USD]', xaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(type='category')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

# Cross Chain Comparison
else:
    st.subheader('Overview')
    df = transactions_overview.query("Blockchain == @options")

    fig = px.bar(df, x='Blockchain', y='Fees', color='Blockchain', title='Total Transaction Fees', log_y=True)
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Fees [USD]', xaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df, x='Blockchain', y='FeeAverage', color='Blockchain', title='Average Fee Amount', log_y=True)
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Average Fee [USD]', xaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.bar(df, x='Blockchain', y='FeeMedian', color='Blockchain', title='Median Fee Amount', log_y=True)
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Median Fee [USD]', xaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')
    df = transactions_daily.query("Blockchain == @options")

    fig = px.line(df, x='Date', y='Fees', color='Blockchain', title='Daily Total Transaction Fees', log_y=True)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Fees [USD]')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.line(df, x='Date', y='FeeAverage', color='Blockchain', title='Daily Average Fee Amount', log_y=True)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Average Fee [USD]')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.line(df, x='Date', y='FeeMedian', color='Blockchain', title='Daily Median Fee Amount', log_y=True)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Median Fee [USD]')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Activity Heatmap')
    c1, c2 = st.columns(2)
    with c1:
        df = transactions_heatmap.query("Blockchain == @options")
        df['Fees'] = df.groupby('Blockchain')['Fees'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        fig = px.density_heatmap(df, x='Blockchain', y='Day', z='Fees', histfunc='avg', title='Daily Heatmap of Normalized Fees')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, coloraxis_colorbar=dict(title='Min/Max'))
        fig.update_xaxes(categoryorder='category ascending')
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = transactions_heatmap.query("Blockchain == @options")
        df['FeeAverage'] = df.groupby('Blockchain')['FeeAverage'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        fig = px.density_heatmap(df, x='Blockchain', y='Day', z='FeeAverage', histfunc='avg', title='Daily Heatmap of Normalized Average Fee')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, coloraxis_colorbar=dict(title='Min/Max'))
        fig.update_xaxes(categoryorder='category ascending')
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = transactions_heatmap.query("Blockchain == @options")
        df['FeeMedian'] = df.groupby('Blockchain')['FeeMedian'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        fig = px.density_heatmap(df, x='Blockchain', y='Day', z='FeeMedian', histfunc='avg', title='Daily Heatmap of Normalized Median Fee')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, coloraxis_colorbar=dict(title='Min/Max'))
        fig.update_xaxes(categoryorder='category ascending')
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = transactions_heatmap.query("Blockchain == @options")
        df['Fees'] = df.groupby('Blockchain')['Fees'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        fig = px.density_heatmap(df, x='Blockchain', y='Hour', z='Fees', histfunc='avg', title='Hourly Heatmap of Normalized Fees', nbinsy=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, coloraxis_colorbar=dict(title='Min/Max'))
        fig.update_xaxes(categoryorder='category ascending')
        fig.update_yaxes(categoryorder='array', categoryarray=week_days, dtick=2)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = transactions_heatmap.query("Blockchain == @options")
        df['FeeAverage'] = df.groupby('Blockchain')['FeeAverage'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        fig = px.density_heatmap(df, x='Blockchain', y='Hour', z='FeeAverage', histfunc='avg', title='Hourly Heatmap of Normalized Average Fee', nbinsy=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, coloraxis_colorbar=dict(title='Min/Max'))
        fig.update_xaxes(categoryorder='category ascending')
        fig.update_yaxes(categoryorder='array', categoryarray=week_days, dtick=2)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = transactions_heatmap.query("Blockchain == @options")
        df['FeeMedian'] = df.groupby('Blockchain')['FeeMedian'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        fig = px.density_heatmap(df, x='Blockchain', y='Hour', z='FeeMedian', histfunc='avg', title='Hourly Heatmap of Normalized Median Fee', nbinsy=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, coloraxis_colorbar=dict(title='Min/Max'))
        fig.update_xaxes(categoryorder='category ascending')
        fig.update_yaxes(categoryorder='array', categoryarray=week_days, dtick=2)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Top Fee Payers')
    df = transactions_fee_payers.query("Blockchain == @options").sort_values(by='Fees', ascending=False).head(30)
    fig = px.bar(df, x='User', y='Fees', color='Blockchain', title='Total Transaction Fees Paid By Top Fee Payers')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Fees [USD]', xaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(type='category')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
