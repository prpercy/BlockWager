import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv("test.env")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('../compiled/cbet_abi.json')) as f:
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
cbet_account_owner_addr = accounts[1]
cbet_account_betting_addr = accounts[0]
user_account_addr_1 = accounts[2]
user_account_addr_2 = accounts[3]
user_account_addr_3 = accounts[4]

WEI_FACTOR = 1000000000000000000
SCORE_SCALING = 100

st.write("(1st Ganache Acct) ---> cbet_account_owner_addr=" + cbet_account_owner_addr)
st.write("(2nd Ganache Acct) ---> cbet_account_betting_addr=" + cbet_account_betting_addr)
st.write("(3rd Ganache Acct) ---> user_account_addr_1=" + user_account_addr_1)
st.write("(4th Ganache Acct) ---> user_account_addr_2=" + user_account_addr_2)
st.write("(5th Ganache Acct) ---> user_account_addr_3" + user_account_addr_3)

st.write("---")

st.write("TEST SETTING UP USER ACCOUNTS")

if st.button("Setup betting account"):
   st.write("cbet_account_owner_addr="+cbet_account_owner_addr)
   st.write("cbet_account_betting_addr="+cbet_account_betting_addr)
   contract.functions.setCbetBettingAddr(cbet_account_betting_addr).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   st.write("Total Ether Betting Balance:"+str(w3.eth.getBalance(cbet_account_betting_addr)/WEI_FACTOR))
      
   st.write("Done")

if st.button("Setup user account"):
   st.write(user_account_addr_1)
   st.write(user_account_addr_2)
   st.write(user_account_addr_3)

   contract.functions.createUserAccount(user_account_addr_1).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createUserAccount(user_account_addr_2).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createUserAccount(user_account_addr_3).transact({'from': cbet_account_owner_addr, 'gas': 1000000})

   st.write("Done")

st.write("---")

st.write("USER ACCOUNT SELECTION")

user_address_lst = [user_account_addr_1, user_account_addr_2, user_account_addr_3]
user_address = st.selectbox('Select User Address', user_address_lst)

def get_balance(user_address):
   (user_balance_wallet_ether, user_balance_wallet_token)              = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether, user_balance_betting_token)            = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether, user_balance_escrow_token)              = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_internal, house_balance_betting_token) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether, house_balance_escrow_token)            = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether)                                       = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether
   (balance_owner_ether, balance_owner_token)                          = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   return (user_balance_wallet_ether,user_balance_wallet_token,user_balance_betting_ether, user_balance_betting_token,user_balance_escrow_ether, user_balance_escrow_token, house_balance_betting_token,house_balance_escrow_ether, house_balance_escrow_token,house_balance_betting_ether,balance_owner_ether, balance_owner_token)                         

def print_delta_balances(user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre,user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post):
   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_pre/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_post/WEI_FACTOR) + " / " + str(user_balance_wallet_token_pre/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_post/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_pre/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_post/WEI_FACTOR) + " / " + str(user_balance_betting_token_pre/WEI_FACTOR) + "-->" + str(user_balance_betting_token_post/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_pre/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_post/WEI_FACTOR) + " / " + str(user_balance_escrow_token_pre/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_post/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_pre/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_post/WEI_FACTOR) + " / " + str(house_balance_betting_token_pre/WEI_FACTOR) + "-->" + str(house_balance_betting_token_post/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_pre/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_post/WEI_FACTOR) + " / " + str(house_balance_escrow_token_pre/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_post/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_pre/WEI_FACTOR) + "-->" + str(balance_owner_ether_post/WEI_FACTOR) + " / " + str(balance_owner_token_pre/WEI_FACTOR) + "-->" + str(balance_owner_token_post/WEI_FACTOR))
                           
                        
if st.button("Check Ether/Token Balances"):

   (user_balance_wallet_ether,user_balance_wallet_token,user_balance_betting_ether,user_balance_betting_token,user_balance_escrow_ether,user_balance_escrow_token,house_balance_betting_token,house_balance_escrow_ether,house_balance_escrow_token,house_balance_betting_ether,balance_owner_ether,balance_owner_token)=get_balance(user_address)

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether/WEI_FACTOR) + " / " + str(user_balance_wallet_token/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether/WEI_FACTOR) + " / " + str(user_balance_betting_token/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether/WEI_FACTOR) + " / " + str(user_balance_escrow_token/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether/WEI_FACTOR) + " / " + str(house_balance_betting_token/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether/WEI_FACTOR) + " / " + str(house_balance_escrow_token/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether/WEI_FACTOR) + " / " + str(balance_owner_token/WEI_FACTOR))

st.write("---")

st.write("TEST PURCHASING AND SELLING OF CBET TOKENS")

amount = st.number_input("Enter how many tokens to purchase",value=1.0)
if st.button("Purchase"):
   st.write(user_address)

   (user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre)=get_balance(user_address)
   
   contract.functions.purchaseCbetTokens().transact({'from': user_address, "value": w3.toWei(amount, "ether"), 'gas': 1000000})

   (user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)=get_balance(user_address)

   print_delta_balances(user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre,user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)
                            
   st.write("Done")

amount = st.number_input("Enter how many tokens to sell",value=1.0)
if st.button("Sell"):
   st.write(user_address)

   (user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre)=get_balance(user_address)
   
   contract.functions.sellCbetTokens(user_address).transact({'from': cbet_account_betting_addr, "value": w3.toWei(amount, "ether"), 'gas': 1000000})

   (user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)=get_balance(user_address)

   print_delta_balances(user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre,user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)
   
   st.write("Done")

st.write("---")

st.write("ASSET SELECTION")

asset_type_lst = ["ETHER", "CBET TOKENS"]
asset_type = st.selectbox('Select Asset Type', asset_type_lst)
is_ether = (asset_type == "ETHER")

st.write("---")

st.write("TEST ETHER/TOKEN DEPOSITS INTO BETTING ACCOUNT")

amount = st.number_input("Enter amount of ether/tokens to deposit",value=1.0)
if st.button("Deposit"):
   st.write(user_address)

   (user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre)=get_balance(user_address)
   
   if (is_ether):
      contract.functions.depositIntoBettingEther().transact({'from': user_address, "value": w3.toWei(amount, "ether"), 'gas': 1000000})
   else:
      contract.functions.depositIntoBettingToken(user_address, w3.toWei(amount, "ether")).transact({'from': user_address, 'gas': 1000000})

   (user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)=get_balance(user_address)

   print_delta_balances(user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre,user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)
   
   st.write("Done")

amount = st.number_input("Enter amount of ether/tokens to withdraw",value=1.0)
if st.button("Withdrawal"):
   st.write(user_address)

   (user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre)=get_balance(user_address)
   
   if (is_ether):
      contract.functions.withdrawFromBettingEther(user_address).transact({'from': cbet_account_betting_addr, "value": w3.toWei(amount, "ether"), 'gas': 1000000})
   else:
      contract.functions.withdrawFromBettingToken(user_address, w3.toWei(amount, "ether")).transact({'from': cbet_account_betting_addr, 'gas': 1000000})

   (user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)=get_balance(user_address)

   print_delta_balances(user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre,user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)
   
   st.write("Done")

st.write("---")

bet_id = 1;
sportbook_id = 2
team_id = 3

st.write("TEST BETTING")
bet_id_place = int(st.number_input("Bet ID (Placing Bet):",value=bet_id))
team_id_place = int(st.number_input("Team ID:",value=team_id))
odds = int(st.number_input("Odds:",value=100))
bet_amount = int(st.number_input("Bet Amount:",value=1.0)) * WEI_FACTOR

if (st.button("Place Moneyline Bet")):
   (user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre)=get_balance(user_address)
   contract.functions.createMoneylineBet(bet_id_place,sportbook_id,team_id_place,odds,user_address,bet_amount,is_ether).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   (user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)=get_balance(user_address)
   print_delta_balances(user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre,user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)
   st.write("Done")

spread = int(st.number_input("Spread:",value=2.)) * SCORE_SCALING

if (st.button("Place Spread Bet")):
   (user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre)=get_balance(user_address)
   contract.functions.createSpreadBet(bet_id_place,sportbook_id,team_id_place,odds,spread,user_address,bet_amount,is_ether).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   (user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)=get_balance(user_address)
   print_delta_balances(user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre,user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)

bet_is_over = st.selectbox('Is Bet Over', [False, True])
total_score = int(st.number_input("OverUnder Score:",value=100)) * SCORE_SCALING

if (st.button("Place Total (Over/Under) Bet")):
   (user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre)=get_balance(user_address)
   contract.functions.createTotalBet(bet_id_place,sportbook_id,team_id_place,odds,bet_is_over,total_score,user_address,bet_amount,is_ether).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   (user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)=get_balance(user_address)
   print_delta_balances(user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre,user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)

bet_id_event = int(st.number_input("Bet ID (Game Event):",value=bet_id))   
winning_team_id = int(st.number_input("Winning Team Id:",value=team_id_place))
winning_score = int(st.number_input("Winning Score:",value=75)) * SCORE_SCALING
losing_score = int(st.number_input("Losing Score:",value=75)) * SCORE_SCALING
if (st.button("Trigger Game Event")):   
   (user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre)=get_balance(user_address)
   contract.functions.gameEvent(bet_id_event, winning_team_id, winning_score, losing_score).transact({'from': cbet_account_betting_addr, 'gas': 1000000})     
   (user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)=get_balance(user_address)
   print_delta_balances(user_balance_wallet_ether_pre,user_balance_wallet_token_pre,user_balance_betting_ether_pre,user_balance_betting_token_pre,user_balance_escrow_ether_pre,user_balance_escrow_token_pre,house_balance_betting_token_pre,house_balance_escrow_ether_pre,house_balance_escrow_token_pre,house_balance_betting_ether_pre,balance_owner_ether_pre,balance_owner_token_pre,user_balance_wallet_ether_post,user_balance_wallet_token_post,user_balance_betting_ether_post,user_balance_betting_token_post,user_balance_escrow_ether_post,user_balance_escrow_token_post,house_balance_betting_token_post,house_balance_escrow_ether_post,house_balance_escrow_token_post,house_balance_betting_ether_post,balance_owner_ether_post,balance_owner_token_post)
   last_payout = contract.functions.getLastPayout().call({'from': cbet_account_owner_addr})
   if (is_ether == True): asset = "ETH"
   if (is_ether == False): asset = "CBET"
   st.write("---")
   st.write(f"Last payout = {str(last_payout)} {asset}")
   bet_id = bet_id + 1
   st.write("Done")             
                
st.write("---")
      
# ToDo:
#  - Add comments
#  - Use SafeMath
#  - Add a bunch of require checks
#  - Decide what should or should not be public
#  - Look for ways to make gas more efficient
#  - On vs. Off chain distribution
#  - Owner cannot deposit into his own betting (withdraw + deposit nto allowed)
#  - Owner cannot bet
#  - Set minimum bet requirement
#  - activate/deactivae account
#  - create separate balance for account balance versus betting (bets in progress)
#  - if game has not started, able to remove funds from betting back to account
#  - be able to withdrawal from account

