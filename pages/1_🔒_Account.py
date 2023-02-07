# Libraries
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from persist import persist, load_widget_state




# Layout
st.set_page_config(page_title='BlockWager | Account', page_icon='🔒', layout='wide')
st.title('🔒 BlockWager Account')

WEI_FACTOR = 10**18

# environment Variables
load_dotenv("./blockwager.env")

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('accountstyle.css')as f:
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


cbet_account_owner_addr = accounts[0]
cbet_account_betting_addr = accounts[1]

if 'cbet_account_owner_addr' not in st.session_state:
    st.session_state['cbet_account_owner_addr'] = cbet_account_owner_addr
    persist('cbet_account_owner_addr')
    
if 'user_account_addr' not in st.session_state:
    st.session_state['user_account_addr'] = ""
    
if 'isRegistered' not in st.session_state:
    st.session_state['isRegistered'] = False
    
def check_registered():
    st.session_state.is_first_time = True
    is_account_active = contract.functions.isUserAccountActive(st.session_state.user_account_address).call({'from': cbet_account_owner_addr})
    st.session_state['user_account_addr'] = st.session_state.user_account_address
    persist("user_account_addr")
    if (is_account_active):
        #user_account_first_name, user_account_last_name = contract.functions.getUserAccountName(st.session_state.user_account_address).call({'from': cbet_account_owner_addr})
        contract.functions.setCbetBettingAddr(cbet_account_betting_addr).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
        st.session_state.isRegistered = True
        
    else:
        st.warning('User is not active', icon="⚠️")
        st.session_state.isRegistered = False
        
def register_new_user():
    try:
        contract.functions.createUserAccount(st.session_state.user_account_address).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
    except Exception as ex:
        st.write(ex.args)
    #user_account_first_name, user_account_last_name = contract.functions.getUserAccountName(st.session_state.user_account_address).call({'from': cbet_account_owner_addr})
    contract.functions.setCbetBettingAddr(cbet_account_betting_addr).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
    st.session_state.isRegistered = True
    st.success(f"{st.session_state.user_account_address} has been successfully registered!", icon="✅")
    st.session_state['user_account_addr'] = st.session_state.user_account_address
    persist("user_account_addr")


def get_balances_pre_action():
    (st.session_state.user_balance_wallet_ether_pre, st.session_state.user_balance_wallet_token_pre) = (w3.eth.getBalance(st.session_state.user_account_addr), contract.functions.balanceCbetTokens(st.session_state.user_account_addr).call())
    (st.session_state.user_balance_betting_ether_pre, st.session_state.user_balance_betting_token_pre) = contract.functions.getBalanceUserBetting(st.session_state.user_account_addr).call()
    (st.session_state.user_balance_escrow_ether_pre, st.session_state.user_balance_escrow_token_pre) = contract.functions.getBalanceUserEscrow(st.session_state.user_account_addr).call()

    (st.session_state.house_balance_betting_ether_pre_internal, st.session_state.house_balance_betting_token_pre) = contract.functions.getBalanceHouseBetting().call()
    (st.session_state.house_balance_escrow_ether_pre, st.session_state.house_balance_escrow_token_pre) = contract.functions.getBalanceHouseEscrow().call()
    (st.session_state.house_balance_betting_ether_pre) = w3.eth.getBalance(cbet_account_betting_addr) - st.session_state.house_balance_escrow_ether_pre
    (st.session_state.balance_owner_ether_pre, st.session_state.balance_owner_token_pre) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

    

with st.form(key='check_registration_form'):
    st.text_input("Wallet public address:", key="user_account_address", value=st.session_state.user_account_addr)
    submit = st.form_submit_button(label='Login to BlockWager', on_click=check_registered)

if (st.session_state.isRegistered != True) and (st.session_state.user_account_addr !=""):
    st.write("This address is not registered with BlockWager. Please register it!")
    st.subheader("New User Registration")
    with st.form(key='registration_form'):
        #st.text_input("First Name:", key="user_first_name")
        #st.text_input("Last Name:", key="user_last_name")
        st.caption(f"Registere user {st.session_state.user_account_addr}")
        submit2 = st.form_submit_button(label='Register new user', on_click=register_new_user)

if st.session_state.user_account_addr and st.session_state.isRegistered:
    #user_account_first_name, user_account_last_name = contract.functions.getUserAccountName(st.session_state.user_account_addr).call({'from': cbet_account_owner_addr})
    get_balances_pre_action()
    st.write("\n")
    st.subheader(f"💳: {st.session_state.user_account_addr}")
    st.write("\n")
    with st.expander("Select Asset Type"):
        asset_type_lst = ["ETHER", "CBET TOKENS"]
        asset_type = st.selectbox('Select Asset Type', asset_type_lst, label_visibility="collapsed")
        is_ether = (asset_type == "ETHER")
    with st.expander(f"Deposit/Withdraw {asset_type} into/from BlockWager Betting Account"):
        st.write("\n")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            amount_deposit_into_betting_account = st.number_input(f"Deposit {asset_type} into Betting Account")
        with c2:
            st.write("\n")
            st.write("\n")
            if st.button("Deposit"):
                if (is_ether):
                    contract.functions.depositIntoBettingEther().transact({'from': st.session_state.user_account_addr, "value": w3.toWei(amount_deposit_into_betting_account, "ether"), 'gas': 1000000})
                else:
                    contract.functions.depositIntoBettingToken(
                        st.session_state.user_account_addr, 
                        w3.toWei(amount_deposit_into_betting_account, "ether")
                    ).transact({'from': st.session_state.user_account_addr, 'gas': 1000000})

        with c3:
            st.write("✢")
            st.write("✢")
            st.write("✢")
        with c4:
            amount_deposit_into_betting_account = st.number_input(f"Withdrawal {asset_type} from Betting Account")
        with c5:
            st.write("\n")
            st.write("\n")
            if st.button("Withdrawal"):
                if (is_ether):
                    contract.functions.withdrawFromBettingEther(st.session_state.user_account_addr).transact(
                        {'from': cbet_account_betting_addr, "value": w3.toWei(amount_deposit_into_betting_account, "ether"), 'gas': 1000000}
                    )
                else:
                    contract.functions.withdrawFromBettingToken(
                        st.session_state.user_account_addr, w3.toWei(amount_deposit_into_betting_account, "ether")
                    ).transact({'from': cbet_account_betting_addr, 'gas': 1000000})


    with st.expander("Purchase/Sell CBET Tokens"):

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            amount_token_purchase = st.number_input("Purchase Tokens")
        with c2:
            st.write("\n")
            st.write("\n")
            if st.button("Purchase"):
                contract.functions.purchaseCbetTokens().transact({'from': st.session_state.user_account_addr, "value": w3.toWei(amount_token_purchase, "ether"), 'gas': 1000000})

        with c3:
            st.write("✢")
            st.write("✢")
            st.write("✢")
        with c4:
            amount_token_sell = st.number_input("Sell Tokens")
        with c5:
            st.write("\n")
            st.write("\n")
            if st.button("Sell"):
                contract.functions.sellCbetTokens(st.session_state.user_account_addr).transact({'from': cbet_account_owner_addr, "value": w3.toWei(amount_token_sell, "ether"), 'gas': 1000000})


    with st.expander(f"Transfer {asset_type} to/from Betting/Escrow Account"):
        st.info(f"**TEST ONLY**")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            amount_transfer_to_escrow = st.number_input(f"Transfer {asset_type} into Escrow Account")
        with c2:
            st.write("\n")
            st.write("\n")            
            if st.button("Transfer to Escrow"):
                contract.functions.transferBettingToEscrow(
                    st.session_state.user_account_addr, w3.toWei(amount_transfer_to_escrow, "ether"), is_ether
                ).transact({'from': st.session_state.user_account_addr, 'gas': 1000000})

        with c3:
            st.write("✢")
            st.write("✢")
            st.write("✢")
        with c4:
            amount_transfer_from_escrow = st.number_input(f"Transfer {asset_type} from Escrow Account")
        with c5:
            st.write("\n")
            st.write("\n")
            if st.button("Transfer from Escrow"):
                contract.functions.transferEscrowToBetting(
                    st.session_state.user_account_addr, w3.toWei(amount_transfer_from_escrow, "ether"), is_ether
                ).transact({'from': st.session_state.user_account_addr, 'gas': 1000000})


    with st.container():

        (st.session_state.user_balance_wallet_ether) = w3.eth.getBalance(st.session_state.user_account_addr)
        (st.session_state.user_balance_wallet_token) = contract.functions.balanceCbetTokens(st.session_state.user_account_addr).call()
        (st.session_state.user_balance_betting_ether, st.session_state.user_balance_betting_token) = contract.functions.getBalanceUserBetting(st.session_state.user_account_addr).call()
        (st.session_state.user_balance_escrow_ether, st.session_state.user_balance_escrow_token) = contract.functions.getBalanceUserEscrow(st.session_state.user_account_addr).call()

        (st.session_state.house_balance_betting_ether_internal, st.session_state.house_balance_betting_token) = contract.functions.getBalanceHouseBetting().call()
        (st.session_state.house_balance_escrow_ether, st.session_state.house_balance_escrow_token) = contract.functions.getBalanceHouseEscrow().call()
        (st.session_state.house_balance_betting_ether) = w3.eth.getBalance(cbet_account_betting_addr) - st.session_state.house_balance_escrow_ether
        (st.session_state.balance_owner_ether, st.session_state.balance_owner_token) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())   

        col1, col2, col3, col4, col5, col6 = st.columns([4,2,2,4,2,2])
        with col1:
            st.subheader("👻")
        with col2:
            st.subheader("Ξ Ether")
        with col3:
            st.subheader("🎲 Cbet")
        with col4:
            st.subheader("🎰")
        with col5:
            st.subheader("Ξ Ether")
        with col6:
            st.subheader("🎲 Cbet")
            
        st.write("---")
        c1, c2, c3, c4, c5, c6 = st.columns([3,2,2,3,2,2])
        with c1:
            st.info('**User Wallet Balance**')
            st.info('**User Betting Balance**')
            st.info('**User Escrow Balance**')
        with c4:
            st.info('**BlockWager/Deployer Balance**')
            st.info('**BlockWager Betting Balance**')
            st.info('**BlockWager Escrow Balance**')
            
        if (st.session_state.is_first_time):
            with c2:
                st.info(format(st.session_state.user_balance_wallet_ether/WEI_FACTOR,'.2f'))
                st.info(format(st.session_state.user_balance_betting_ether/WEI_FACTOR,'.2f'))
                st.info(format(st.session_state.user_balance_escrow_ether/WEI_FACTOR,'.2f'))
            with c3:
                st.info(format(st.session_state.user_balance_wallet_token/WEI_FACTOR,'.2f'))
                st.info(format(st.session_state.user_balance_betting_token/WEI_FACTOR,'.2f'))
                st.info(format(st.session_state.user_balance_escrow_token/WEI_FACTOR,'.2f'))
            with c5:
                st.info(format(st.session_state.balance_owner_ether/WEI_FACTOR,'.2f'))
                st.info(format(st.session_state.house_balance_betting_ether/WEI_FACTOR,'.2f'))
                st.info(format(st.session_state.house_balance_escrow_ether/WEI_FACTOR,'.2f'))
            with c6:
                st.info(format(st.session_state.balance_owner_token/WEI_FACTOR,'.2g'))
                st.info(format(st.session_state.house_balance_betting_token/WEI_FACTOR,'.2g'))
                st.info(format(st.session_state.house_balance_escrow_token/WEI_FACTOR,'.2g'))
        else:
            with c2:
                st.info(f"{format(st.session_state.user_balance_wallet_ether_pre/WEI_FACTOR,'.2f')} ➡️ {format(st.session_state.user_balance_wallet_ether/WEI_FACTOR,'.2f')}")
                st.info(f"{format(st.session_state.user_balance_betting_ether_pre/WEI_FACTOR,'.2f')} ➡️ {format(st.session_state.user_balance_betting_ether/WEI_FACTOR,'.2f')}")
                st.info(f"{format(st.session_state.user_balance_escrow_ether_pre/WEI_FACTOR,'.2f')} ➡️ {format(st.session_state.user_balance_escrow_ether/WEI_FACTOR,'.2f')}")
            with c3:
                st.info(f"{format(st.session_state.user_balance_wallet_token_pre/WEI_FACTOR,'.2f')} ➡️ {format(st.session_state.user_balance_wallet_token/WEI_FACTOR,'.2f')}")
                st.info(f"{format(st.session_state.user_balance_betting_token_pre/WEI_FACTOR,'.2f')} ➡️ {format(st.session_state.user_balance_betting_token/WEI_FACTOR,'.2f')}")
                st.info(f"{format(st.session_state.user_balance_escrow_token_pre/WEI_FACTOR,'.2f')} ➡️ {format(st.session_state.user_balance_escrow_token/WEI_FACTOR,'.2f')}")
            with c5:
                st.info(f"{format(st.session_state.balance_owner_ether_pre/WEI_FACTOR,'.2f')} ➡️ {format(st.session_state.balance_owner_ether/WEI_FACTOR,'.2f')}")
                st.info(f"{format(st.session_state.house_balance_betting_ether_pre/WEI_FACTOR,'.2f')} ➡️ {format(st.session_state.house_balance_betting_ether/WEI_FACTOR,'.2f')}")
                st.info(f"{format(st.session_state.house_balance_escrow_ether_pre/WEI_FACTOR,'.2f')} ➡️ {format(st.session_state.house_balance_escrow_ether/WEI_FACTOR,'.2f')}")
            with c6:
                st.info(f"{format(st.session_state.balance_owner_token_pre/WEI_FACTOR,'.2g')} ➡️ {format(st.session_state.balance_owner_token/WEI_FACTOR,'.2g')}")
                st.info(f"{format(st.session_state.house_balance_betting_token_pre/WEI_FACTOR,'.2g')} ➡️ {format(st.session_state.house_balance_betting_token/WEI_FACTOR,'.2g')}")
                st.info(f"{format(st.session_state.house_balance_escrow_token_pre/WEI_FACTOR,'.2g')} ➡️ {format(st.session_state.house_balance_escrow_token/WEI_FACTOR,'.2g')}")

        st.write("---")
        st.write("\n")
        st.write("\n")
      
    st.session_state.is_first_time = False
