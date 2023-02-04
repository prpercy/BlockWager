# Libraries
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st


# environment Variables
load_dotenv("./blockwager.env")

# Layout
st.set_page_config(page_title='BlockWager | Account', page_icon='🔒', layout='wide')
st.title('🔒 Account')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
################################################################################



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

#################################################################################
## Extract Ganache Accounts
#################################################################################

accounts = w3.eth.accounts

#################################################################################
## Assign accounts
#################################################################################

st.markdown("---")
cbet_account_wallet_addr = accounts[0]
cbet_account_owner_addr = accounts[1]

if 'isRegistered' not in st.session_state:
    st.session_state['isRegistered'] = False
    
def check_registered():
    user_account_first_name_1, user_account_last_name_1 = contract.functions.getUserAccountName(st.session_state.user_accountr_addr).call({'from': cbet_account_owner_addr})
    if user_account_first_name_1 != "":
        st.session_state.isRegistered = True
    else:
        st.session_state.isRegistered = False
        
def register_new_user():
    try:
           contract.functions.createUserAccount(
               st.session_state.user_accountr_addr, st.session_state.user_first_name, st.session_state.user_last_name, st.session_state.user_user_name, st.session_state.user_user_password
           ).transact(
               {'from': cbet_account_owner_addr, 'gas': 1000000}
           )
    except Exception as ex:
           st.write(ex.args)
    user_account_first_name_1, user_account_last_name_1 = contract.functions.getUserAccountName(st.session_state.user_accountr_addr).call({'from': cbet_account_owner_addr})
    st.session_state.isRegistered = True
    st.write(f"{user_account_first_name_1} {user_account_last_name_1} has been successfully registered!")
    
with st.form(key='check_registration_form'):
    st.text_input("Please provide your ETH wallet public address", key="user_accountr_addr")
    submit = st.form_submit_button(label='Check if address is registered with BlockWager', on_click=check_registered)

if (st.session_state.isRegistered != True) and (st.session_state.user_accountr_addr !=""):
    st.write("This address is not registered with BlockWager. Please register it!")
    st.subheader("Register a new user")
    with st.form(key='registration_form'):
        st.text_input("Enter your first name", key="user_first_name")
        st.text_input("Enter your last name", key="user_last_name")
        st.text_input("Enter your user name", key="user_user_name")
        st.text_input("Enter your user password", key="user_user_password")
        submit2 = st.form_submit_button(label='Register new user', on_click=register_new_user)

if st.session_state.user_accountr_addr and st.session_state.isRegistered:
    user_account_first_name_1, user_account_last_name_1 = contract.functions.getUserAccountName(st.session_state.user_accountr_addr).call({'from': cbet_account_owner_addr})
    st.subheader(f"Welcome {user_account_first_name_1} {user_account_last_name_1}!!!")
    st.subheader("Deposit into your BlockWager account")
    deposit_amount = st.number_input("Enter the amount you wish to deposit")
    if st.button("Make deposit"):
        print("are you coming here...")
        contract.functions.depositUserAccountEther(cbet_account_wallet_addr).transact({'from': st.session_state.user_accountr_addr, "value": w3.toWei(deposit_amount, "ether"), 'gas': 1000000})
        st.write(f"You successfully deposited {deposit_amount} ETH into your BlockWager account!")

    st.subheader("Withdraw from your BlockWager account")
    withdraw_amount = st.number_input("Enter the amount you wish to withdraw")
    if st.button("Make withdrawal"):
       contract.functions.withdrawUserAccountEther(st.session_state.user_accountr_addr).transact({'from': cbet_account_wallet_addr, "value": w3.toWei(withdraw_amount, "ether"), 'gas': 1000000})
       st.write(f"You successfully withdrew {withdraw_amount} ETH from your BlockWager account")

    st.subheader("Your BlockWager account balance")
    balance = contract.functions.getBalanceUserAccountEther().call({'from': st.session_state.user_accountr_addr})
    st.write(f"{balance/10**18} ETH")
