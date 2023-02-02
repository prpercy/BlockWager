# Libraries
import streamlit as st
from PIL import Image

# Layout
st.set_page_config(page_title='BlockWager | Home', page_icon='🎰', layout='wide')
st.title('Welcome to BlockWager 🎰')

# Content
c1, c2, c3, c4, c5 = st.columns(5)
c1.image(Image.open('images/MLB.png').resize((100,100)))
c2.image(Image.open('images/MLS.png').resize((100,100)))
c3.image(Image.open('images/NBA.png').resize((50,100)))
c4.image(Image.open('images/NFL.png').resize((80,100)))
c5.image(Image.open('images/NHL.png').resize((100,100)))


st.write(
    """
    Introducing the revolutionary new sports betting app built on the cutting-edge technology of web 3
    and blockchain! Say goodbye to traditional centralized sports betting platforms and experience the
    freedom and security of a semi-decentralized sports betting experience. With our user-friendly app,
    you can now place bets on your favorite sports with ease and confidence, knowing that your funds and
    information are protected by the secure and transparent blockchain technology. 
    
    So what are you waiting for? Join the future of sports betting today!

    """
)

st.subheader('Getting Started')
st.write(
    """
    Connect via Metamask to use your existing wallet and bet using your ETH balance or purchase our own 
    proprietary token BlockChips. 

    This tool is designed and structured in multiple **Pages** that are accessible using the sidebar.
    Each of these Pages addresses a different sport. Within each segment you are able to filter your desired
    team and game based on the most recent avaialble odds.
    """
)

st.write('---')

c1 = st.info('**GitHub: [@ppercy/BlockWager](https://github.com/prpercy/BlockWager)**', icon="💻")
