# Libraries
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from persist import persist, load_widget_state


WEI_FACTOR = 10**18

# environment Variables
load_dotenv("./blockwager.env")

# Layout
st.set_page_config(page_title='BlockWager | Account', page_icon='🔒', layout='wide')
st.title('🔒 BlockWager Account')

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
cbet_account_owner_addr = accounts[0]
cbet_account_betting_addr = accounts[1]
st.write(f"Betting address -> {cbet_account_betting_addr}")
st.write(f"cbet_account_owner_addr address -> {cbet_account_owner_addr}")


if 'user_account_addr' not in st.session_state:
    st.session_state['user_account_addr'] = ""
    persist("user_account_addr")
    
if 'isRegistered' not in st.session_state:
    st.session_state['isRegistered'] = False
    
def check_registered():
    st.session_state.is_first_time = True
    is_account_active = contract.functions.isUserAccountActive(st.session_state.user_account_address).call({'from': cbet_account_owner_addr})
    if (is_account_active):
        user_account_first_name, user_account_last_name = contract.functions.getUserAccountName(st.session_state.user_account_address).call({'from': cbet_account_owner_addr})
        contract.functions.setCbetBettingAddr(cbet_account_betting_addr).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
        st.session_state.isRegistered = True
        st.session_state['user_account_addr'] = st.session_state.user_account_address
        persist("user_account_addr")
    else:
        st.session_state.isRegistered = False
        
def register_new_user():
    try:
       contract.functions.createUserAccount(
          st.session_state.user_account_address, st.session_state.user_first_name, st.session_state.user_last_name
       ).transact(
          {'from': cbet_account_owner_addr, 'gas': 1000000}
       )
    except Exception as ex:
           st.write(ex.args)
    user_account_first_name, user_account_last_name = contract.functions.getUserAccountName(st.session_state.user_account_address).call({'from': cbet_account_owner_addr})
    contract.functions.setCbetBettingAddr(cbet_account_betting_addr).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
    st.session_state.isRegistered = True
    st.write(f"{user_account_first_name} {user_account_last_name} has been successfully registered!")
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
    st.text_input("Wallet public address:", key="user_account_address")
    submit = st.form_submit_button(label='Login to BlockWager', on_click=check_registered)

if (st.session_state.isRegistered != True) and (st.session_state.user_account_addr !=""):
    st.write("This address is not registered with BlockWager. Please register it!")
    st.subheader("New User Registration")
    with st.form(key='registration_form'):
        st.text_input("First Name:", key="user_first_name")
        st.text_input("Last Name:", key="user_last_name")
        submit2 = st.form_submit_button(label='Register new user', on_click=register_new_user)

if st.session_state.user_account_addr and st.session_state.isRegistered:
    user_account_first_name, user_account_last_name = contract.functions.getUserAccountName(st.session_state.user_account_addr).call({'from': cbet_account_owner_addr})
    st.write("---")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader(f"ACCOUNT: {user_account_first_name} {user_account_last_name}!!!")
        st.write("---")
        st.subheader("PURCHASE/SELL CBET TOKENS:")
        amount_token_purchase = st.number_input("Purchase Tokens")
        if st.button("Purchase"):
           get_balances_pre_action()
           contract.functions.purchaseCbetTokens().transact({'from': st.session_state.user_account_addr, "value": w3.toWei(amount_token_purchase, "ether"), 'gas': 1000000})
        amount_token_sell = st.number_input("Sell Tokens")
        if st.button("Sell"):
           get_balances_pre_action()
           contract.functions.sellCbetTokens(st.session_state.user_account_addr).transact({'from': cbet_account_owner_addr, "value": w3.toWei(amount_token_sell, "ether"), 'gas': 1000000})

        st.write("---")
        st.subheader("ASSET SELECTION:")
        asset_type_lst = ["ETHER", "CBET TOKENS"]
        asset_type = st.selectbox('Select Asset Type', asset_type_lst)
        is_ether = (asset_type == "ETHER")

        st.write("---")
        st.subheader(f"DEPOSIT/WITHDRAW {asset_type} INTO BLOCKWAGER BETTING ACCOUNT:")
        amount_deposit_into_betting_account = st.number_input(f"Deposit {asset_type} into Betting Account")
        if st.button("Deposit"):
           get_balances_pre_action()
           if (is_ether):
              contract.functions.depositIntoBettingEther().transact({'from': st.session_state.user_account_addr, "value": w3.toWei(amount_deposit_into_betting_account, "ether"), 'gas': 1000000})
           else:
              contract.functions.depositIntoBettingToken(st.session_state.user_account_addr, w3.toWei(amount_deposit_into_betting_account, "ether")).transact({'from': st.session_state.user_account_addr, 'gas': 1000000})
        amount_deposit_into_betting_account = st.number_input(f"Withdrawal {asset_type} from Betting Account")
        if st.button("Withdrawal"):
           get_balances_pre_action()
           if (is_ether):
              contract.functions.withdrawFromBettingEther(st.session_state.user_account_addr).transact({'from': cbet_account_betting_addr, "value": w3.toWei(amount_deposit_into_betting_account, "ether"), 'gas': 1000000})
           else:
              contract.functions.withdrawFromBettingToken(st.session_state.user_account_addr, w3.toWei(amount_deposit_into_betting_account, "ether")).transact({'from': cbet_account_betting_addr, 'gas': 1000000})

        st.write("---")
        st.subheader(f"TRANSFER {asset_type} TO/FROM BETTING/ESCROW ACCOUNT  (*** TEST ONLY, MOVE TO GAME BETTING PAGE WHEN READY ***):")
        amount_transfer_to_escrow = st.number_input(f"Transfer {asset_type} into Escrow Account")
        if st.button("Transfer to Escrow"):
           get_balances_pre_action()
           contract.functions.transferBettingToEscrow(st.session_state.user_account_addr, w3.toWei(amount_transfer_to_escrow, "ether"), is_ether).transact({'from': st.session_state.user_account_addr, 'gas': 1000000})
        amount_transfer_from_escrow = st.number_input(f"Transfer {asset_type} from Escrow Account")
        if st.button("Transfer from Escrow"):
           get_balances_pre_action()
           contract.functions.transferEscrowToBetting(st.session_state.user_account_addr, w3.toWei(amount_transfer_from_escrow, "ether"), is_ether).transact({'from': st.session_state.user_account_addr, 'gas': 1000000})

        st.write("---")
    with c2:
        st.subheader("Account Balances:")
        st.write("---")

        st.session_state.user_balance_wallet_ether = w3.eth.getBalance(st.session_state.user_account_addr)
        st.session_state.user_balance_wallet_token = contract.functions.balanceCbetTokens(st.session_state.user_account_addr).call()
        (st.session_state.user_balance_betting_ether, st.session_state.user_balance_betting_token) = contract.functions.getBalanceUserBetting(st.session_state.user_account_addr).call()
        (st.session_state.user_balance_escrow_ether, st.session_state.user_balance_escrow_token) = contract.functions.getBalanceUserEscrow(st.session_state.user_account_addr).call()

        st.write("User Balances (ETH / CBET):")
        if (st.session_state.is_first_time):
            st.write("User Wallet Balance ==> ETH:" + str(st.session_state.user_balance_wallet_ether/WEI_FACTOR)         + " / CBET:" + str(st.session_state.user_balance_wallet_token/WEI_FACTOR))
            st.write("BlockWager Betting Balance ==> ETH:" + str(st.session_state.user_balance_betting_ether/WEI_FACTOR) + " / CBET:" + str(st.session_state.user_balance_betting_token/WEI_FACTOR))
            st.write("BlockWager Escrow Balance ==> ETH:" + str(st.session_state.user_balance_escrow_ether/WEI_FACTOR)   + " / CBET:" + str(st.session_state.user_balance_escrow_token/WEI_FACTOR))       
        else:
            if (
                (st.session_state.user_balance_wallet_ether_pre != st.session_state.user_balance_wallet_ether) and
                (st.session_state.user_balance_wallet_token_pre == st.session_state.user_balance_wallet_token)
            ):
                st.write(
                    "User Wallet Balance ==> ETH:" + str(st.session_state.user_balance_wallet_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.user_balance_wallet_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_wallet_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.user_balance_wallet_ether_pre == st.session_state.user_balance_wallet_ether) and
                (st.session_state.user_balance_wallet_token_pre != st.session_state.user_balance_wallet_token)
            ):
                st.write(
                    "User Wallet Balance ==> ETH:" + str(st.session_state.user_balance_wallet_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_wallet_token_pre/WEI_FACTOR)  + "-->" + str(st.session_state.user_balance_wallet_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.user_balance_wallet_ether_pre != st.session_state.user_balance_wallet_ether) and
                (st.session_state.user_balance_wallet_token_pre != st.session_state.user_balance_wallet_token)
            ):
                st.write(
                    "User Wallet Balance ==> ETH:" + str(st.session_state.user_balance_wallet_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.user_balance_wallet_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_wallet_token_pre/WEI_FACTOR) + "-->" + str(st.session_state.user_balance_wallet_token/WEI_FACTOR)
                )
            else :
                st.write(
                    "User Wallet Balance ==> ETH:" + str(st.session_state.user_balance_wallet_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_wallet_token/WEI_FACTOR)
                )

            if (
                (st.session_state.user_balance_betting_ether_pre != st.session_state.user_balance_betting_ether) and
                (st.session_state.user_balance_betting_token_pre == st.session_state.user_balance_betting_token)
            ):
                st.write(
                    "BlockWager Betting Balance ==> ETH:" + str(st.session_state.user_balance_betting_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.user_balance_betting_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_betting_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.user_balance_betting_ether_pre == st.session_state.user_balance_betting_ether) and
                (st.session_state.user_balance_betting_token_pre != st.session_state.user_balance_betting_token)
            ):
                st.write(
                    "BlockWager Betting Balance ==> ETH:" + str(st.session_state.user_balance_betting_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_betting_token_pre/WEI_FACTOR)  + "-->" + str(st.session_state.user_balance_betting_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.user_balance_betting_ether_pre != st.session_state.user_balance_betting_ether) and
                (st.session_state.user_balance_betting_token_pre != st.session_state.user_balance_betting_token)
            ):
                st.write(
                    "BlockWager Betting Balance ==> ETH:" + str(st.session_state.user_balance_betting_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.user_balance_betting_ether/WEI_FACTOR) 
                    + " / CBET:" + str(st.session_state.user_balance_betting_token_pre/WEI_FACTOR) + "-->" + str(st.session_state.user_balance_betting_token/WEI_FACTOR)
                )
            else:
                st.write(
                    "BlockWager Betting Balance ==> ETH:" + str(st.session_state.user_balance_betting_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_betting_token/WEI_FACTOR)
                )

            if (
                (st.session_state.user_balance_escrow_ether_pre != st.session_state.user_balance_escrow_ether) and
                (st.session_state.user_balance_escrow_token_pre == st.session_state.user_balance_escrow_token)
            ):
                st.write(
                    "BlockWager Escrow Balance ==> ETH:" + str(st.session_state.user_balance_escrow_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.user_balance_escrow_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_escrow_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.user_balance_escrow_ether_pre == st.session_state.user_balance_escrow_ether) and
                (st.session_state.user_balance_escrow_token_pre != st.session_state.user_balance_escrow_token)
            ):
                st.write(
                    "BlockWager Escrow Balance ==> ETH:" + str(st.session_state.user_balance_escrow_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_escrow_token_pre/WEI_FACTOR)  + "-->" + str(st.session_state.user_balance_escrow_token/WEI_FACTOR)
                )
            elif ( 
                (st.session_state.user_balance_escrow_ether_pre != st.session_state.user_balance_escrow_ether) and
                (st.session_state.user_balance_escrow_token_pre != st.session_state.user_balance_escrow_token)
            ):
                st.write(
                    "BlockWager Escrow Balance ==> ETH:" + str(st.session_state.user_balance_escrow_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.user_balance_escrow_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_escrow_token_pre/WEI_FACTOR) + "-->" + str(st.session_state.user_balance_escrow_token/WEI_FACTOR)
                )
            else:
                st.write(
                    "BlockWager Escrow Balance ==> ETH:" + str(st.session_state.user_balance_escrow_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.user_balance_escrow_token/WEI_FACTOR)
                )

        (st.session_state.house_balance_betting_ether_internal, st.session_state.house_balance_betting_token) = contract.functions.getBalanceHouseBetting().call()
        (st.session_state.house_balance_escrow_ether, st.session_state.house_balance_escrow_token) = contract.functions.getBalanceHouseEscrow().call()
        (st.session_state.house_balance_betting_ether) = w3.eth.getBalance(cbet_account_betting_addr) - st.session_state.house_balance_escrow_ether
        (st.session_state.balance_owner_ether, st.session_state.balance_owner_token) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())    

        st.write("---")
        st.write("House Balances (ETH / CBET):")
        if (st.session_state.is_first_time):
           st.write("Owner/Deployer Balance ==> ETH:" + str(st.session_state.balance_owner_ether/WEI_FACTOR)        + " / CBET:" + str(st.session_state.balance_owner_token/WEI_FACTOR))
           st.write("House Betting Balance ==> ETH:" + str(st.session_state.house_balance_betting_ether/WEI_FACTOR) + " / CBET:" + str(st.session_state.house_balance_betting_token/WEI_FACTOR))
           st.write("House Escrow Balance ==> ETH:" + str(st.session_state.house_balance_escrow_ether/WEI_FACTOR)   + " / CBET:" + str(st.session_state.house_balance_escrow_token/WEI_FACTOR))
        else:

            if (
                (st.session_state.balance_owner_ether_pre != st.session_state.balance_owner_ether) and
                (st.session_state.balance_owner_token_pre == st.session_state.balance_owner_token)
            ):
                st.write(
                    "Owner/Deployer Balance ==> ETH:" + str(st.session_state.balance_owner_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.balance_owner_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.balance_owner_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.balance_owner_ether_pre == st.session_state.balance_owner_ether) and
                (st.session_state.balance_owner_token_pre != st.session_state.balance_owner_token)
            ):
                st.write(
                    "Owner/Deployer Balance ==> ETH:" + str(st.session_state.balance_owner_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.balance_owner_token_pre/WEI_FACTOR)  + "-->" + str(st.session_state.balance_owner_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.balance_owner_ether_pre != st.session_state.balance_owner_ether) and
                (st.session_state.balance_owner_token_pre != st.session_state.balance_owner_token)
            ):
                st.write(
                    "Owner/Deployer Balance ==> ETH:" + str(st.session_state.balance_owner_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.balance_owner_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.balance_owner_token_pre/WEI_FACTOR) + "-->" + str(st.session_state.balance_owner_token/WEI_FACTOR)
                )
            else :
                 st.write(
                     "Owner/Deployer Balance ==> ETH:" + str(st.session_state.balance_owner_ether/WEI_FACTOR) 
                     + " / CBET:" + str(st.session_state.balance_owner_token/WEI_FACTOR)
                 )

            if (
                (st.session_state.house_balance_betting_ether_pre != st.session_state.house_balance_betting_ether) and
                (st.session_state.house_balance_betting_token_pre == st.session_state.house_balance_betting_token)
            ):
                st.write(
                    "House Betting Balance ==> ETH:" + str(st.session_state.house_balance_betting_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.house_balance_betting_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.house_balance_betting_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.house_balance_betting_ether_pre == st.session_state.house_balance_betting_ether) and
                (st.session_state.house_balance_betting_token_pre != st.session_state.house_balance_betting_token)
            ):
                st.write(
                    "House Betting Balance ==> ETH:" + str(st.session_state.house_balance_betting_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.house_balance_betting_token_pre/WEI_FACTOR)  + "-->" + str(st.session_state.house_balance_betting_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.house_balance_betting_ether_pre != st.session_state.house_balance_betting_ether) and
                (st.session_state.house_balance_betting_token_pre != st.session_state.house_balance_betting_token)
            ):
                st.write(
                    "House Betting Balance ==> ETH:" + str(st.session_state.house_balance_betting_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.house_balance_betting_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.house_balance_betting_token_pre/WEI_FACTOR) + "-->" + str(st.session_state.house_balance_betting_token/WEI_FACTOR)
                )
            else :
                 st.write(
                     "House Betting Balance ==> ETH:" + str(st.session_state.house_balance_betting_ether/WEI_FACTOR)
                     + " / CBET:" + str(st.session_state.house_balance_betting_token/WEI_FACTOR)
                 )

            if (
                (st.session_state.house_balance_escrow_ether_pre != st.session_state.house_balance_escrow_ether) and
                (st.session_state.house_balance_escrow_token_pre == st.session_state.house_balance_escrow_token)
            ):
                st.write(
                    "House Escrow Balance ==> ETH:" + str(st.session_state.house_balance_escrow_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.house_balance_escrow_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.house_balance_escrow_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.house_balance_escrow_ether_pre == st.session_state.house_balance_escrow_ether) and
                (st.session_state.house_balance_escrow_token_pre != st.session_state.house_balance_escrow_token)
            ):
                st.write(
                    "House Escrow Balance ==> ETH:" + str(st.session_state.house_balance_escrow_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.house_balance_escrow_token_pre/WEI_FACTOR)  + "-->" + str(st.session_state.house_balance_escrow_token/WEI_FACTOR)
                )
            elif (
                (st.session_state.house_balance_escrow_ether_pre != st.session_state.house_balance_escrow_ether) and
                (st.session_state.house_balance_escrow_token_pre != st.session_state.house_balance_escrow_token)
            ):
                st.write(
                    "House Escrow Balance ==> ETH:" + str(st.session_state.house_balance_escrow_ether_pre/WEI_FACTOR)  + "-->" + str(st.session_state.house_balance_escrow_ether/WEI_FACTOR)
                    + " / CBET:" + str(st.session_state.house_balance_escrow_token_pre/WEI_FACTOR) + "-->" + str(st.session_state.house_balance_escrow_token/WEI_FACTOR)
                )
            else :
                 st.write(
                     "House Escrow Balance ==> ETH:" + str(st.session_state.house_balance_escrow_ether/WEI_FACTOR)
                     + " / CBET:" + str(st.session_state.house_balance_escrow_token/WEI_FACTOR)
                 )

        st.write("---")
      
    st.session_state.is_first_time = False
