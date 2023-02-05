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
SPREAD_FACTOR = 100
TOTAL_FACTOR = 100

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

   contract.functions.createUserAccount(user_account_addr_1, "FirstName1", "LastName1").transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createUserAccount(user_account_addr_2, "FirstName2", "LastName2").transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createUserAccount(user_account_addr_3, "FirstName3", "LastName3").transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   
   (user_account_first_name_1, user_account_last_name_1) = contract.functions.getUserAccountName(user_account_addr_1).call({'from': cbet_account_owner_addr})
   (user_account_first_name_2, user_account_last_name_2) = contract.functions.getUserAccountName(user_account_addr_2).call({'from': cbet_account_owner_addr})
   (user_account_first_name_3, user_account_last_name_3) = contract.functions.getUserAccountName(user_account_addr_3).call({'from': cbet_account_owner_addr})

   st.write(user_account_first_name_1+" "+user_account_last_name_1)
   st.write(user_account_first_name_2+" "+user_account_last_name_2)
   st.write(user_account_first_name_3+" "+user_account_last_name_3)

   st.write("Done")

st.write("---")

st.write("USER ACCOUNT SELECTION")

user_address_lst = [user_account_addr_1, user_account_addr_2, user_account_addr_3]
user_address = st.selectbox('Select User Address', user_address_lst)

if st.button("Check Ether/Token Balances"):

   (user_balance_wallet_ether, user_balance_wallet_token) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether, user_balance_betting_token) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether, user_balance_escrow_token) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_internal, house_balance_betting_token) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether, house_balance_escrow_token) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether
   (balance_owner_ether, balance_owner_token) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether/WEI_FACTOR) + " / " + str(user_balance_wallet_token/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether/WEI_FACTOR) + " / " + str(user_balance_betting_token/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether/WEI_FACTOR) + " / " + str(user_balance_escrow_token/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether/WEI_FACTOR) + " / " + str(house_balance_betting_token/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether/WEI_FACTOR) + " / " + str(house_balance_escrow_token/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether/WEI_FACTOR) + " / " + str(balance_owner_token/WEI_FACTOR))

st.write("---")

st.write("TEST PURCHASING AND SELLING OF CBET TOKENS")

amount = st.text_input("Enter how many tokens to purchase")
if st.button("Purchase"):
   st.write(user_address)

   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())
   
   contract.functions.purchaseCbetTokens().transact({'from': user_address, "value": w3.toWei(amount, "ether"), 'gas': 1000000})

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))
   
   st.write("Done")

amount = st.text_input("Enter how many tokens to sell")
if st.button("Sell"):
   st.write(user_address)

   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())
   
   contract.functions.sellCbetTokens(user_address).transact({'from': cbet_account_owner_addr, "value": w3.toWei(amount, "ether"), 'gas': 1000000})

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))
   
   st.write("Done")

st.write("---")

st.write("ASSET SELECTION")

asset_type_lst = ["ETHER", "CBET TOKENS"]
asset_type = st.selectbox('Select Asset Type', asset_type_lst)
is_ether = (asset_type == "ETHER")

st.write("---")

st.write("TEST ETHER/TOKEN DEPOSITS INTO BETTING ACCOUNT")

amount = st.text_input("Enter amount of ether/tokens to deposit")
if st.button("Deposit"):
   st.write(user_address)

   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())
   
   if (is_ether):
      contract.functions.depositIntoBettingEther().transact({'from': user_address, "value": w3.toWei(amount, "ether"), 'gas': 1000000})
   else:
      contract.functions.depositIntoBettingToken(user_address, w3.toWei(amount, "ether")).transact({'from': user_address, 'gas': 1000000})

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))
   
   st.write("Done")

amount = st.text_input("Enter amount of ether/tokens to withdraw")
if st.button("Withdrawal"):
   st.write(user_address)

   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())
   
   if (is_ether):
      contract.functions.withdrawFromBettingEther(user_address).transact({'from': cbet_account_betting_addr, "value": w3.toWei(amount, "ether"), 'gas': 1000000})
   else:
      contract.functions.withdrawFromBettingToken(user_address, w3.toWei(amount, "ether")).transact({'from': cbet_account_betting_addr, 'gas': 1000000})

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))
   
   st.write("Done")

st.write("---")

st.write("TEST TRANSFERRING ETHER/TOKEN TO/FROM BETTING/ESCROW ACCOUNT")
   
amount = st.text_input("Enter amount of ether/tokens to transfer from betting to escrow accont")
if st.button("Transfer Betting To Escrow Account"):
   st.write(user_address)

   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())
   
   contract.functions.transferBettingToEscrow(user_address, w3.toWei(amount, "ether"), is_ether).transact({'from': user_address, 'gas': 1000000})

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))
   
   st.write("Done")

st.write("---")

amount = st.text_input("Enter amount of ether/tokens to transfer from escrow to betting accont")
if st.button("Transfer Escrow To Betting Account"):
   st.write(user_address)

   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())
   
   contract.functions.transferEscrowToBetting(user_address, w3.toWei(amount, "ether"), is_ether).transact({'from': user_address, 'gas': 1000000})

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))
   
   st.write("Done")

st.write("---")

st.write("TEST PLACE BETS")

if st.button("Place Bet #1, Moneyline, 1 Eth"):
   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   bet_id = 1 
   sportbook = "FanDuel" 
   team = "Philadelphia Eagles"
   odds = -156
   addr = user_address
   bet_amount = (1 * WEI_FACTOR)
   is_ether = True
   
   contract.functions.createMoneylineBet(bet_id,sportbook,team,odds,addr,bet_amount,is_ether).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   
   st.write(f"BetType: {contract.functions.getBetType(bet_id).call({'from': cbet_account_owner_addr})}")
   (sportbook,gameStatus,team,odds) = contract.functions.getBetMoneyLineOdds(bet_id).call({'from': cbet_account_owner_addr})
   (addr,bet_amount,is_ether) = contract.functions.getBetMoneyLineBet(bet_id).call({'from': cbet_account_owner_addr})
   st.write(f"sportbook: {sportbook}")
   st.write(f"gameStatus: {gameStatus}")
   st.write(f"team: {team}")
   st.write(f"odds: {odds}")
   st.write(f"addr: {addr}")
   st.write(f"bet_amount: {bet_amount/WEI_FACTOR}")
   st.write(f"is_ether: {str(is_ether)}")

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))

   st.write("Done")

if st.button("Place Bet #2, Spread, 1 Eth"):
   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())


   bet_id = 1 
   sportbook = "FanDuel" 
   team = "San Fransisco"
   odds = 100
   spread = int((2.5 * SPREAD_FACTOR))
   addr = user_address
   bet_amount = (1 * WEI_FACTOR)
   is_ether = True
   
   contract.functions.createSpreadBet(bet_id,sportbook,team,odds,spread,addr,bet_amount,is_ether).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   
   st.write(f"BetType: {contract.functions.getBetType(bet_id).call({'from': cbet_account_owner_addr})}")
   (sportbook,gameStatus,team,odds,spread) = contract.functions.getBetSpreadOdds(bet_id).call({'from': cbet_account_owner_addr})
   (addr,bet_amount,is_ether) = contract.functions.getBetSpreadBet(bet_id).call({'from': cbet_account_owner_addr})
   st.write(f"sportbook: {sportbook}")
   st.write(f"gameStatus: {gameStatus}")
   st.write(f"team: {team}")
   st.write(f"odds: {odds}")
   st.write(f"spread: {spread}")
   st.write(f"addr: {addr}")
   st.write(f"bet_amount: {bet_amount/WEI_FACTOR}")
   st.write(f"is_ether: {str(is_ether)}")

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))

   st.write("Done")

if st.button("Place Bet #3, Total, 1 Eth"):
   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())
 
   bet_id = 1 
   sportbook = "FanDuel" 
   team = "San Fransisco"
   odds = 100
   is_over = True
   total = int(46.5 * TOTAL_FACTOR)
   addr = user_address
   bet_amount = (1 * WEI_FACTOR)
   is_ether = True
   
   contract.functions.createTotalBet(bet_id,sportbook,team,odds,is_over,total,addr,bet_amount,is_ether).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   
   st.write(f"BetType: {contract.functions.getBetType(bet_id).call({'from': cbet_account_owner_addr})}")
   (sportbook,gameStatus,team,odds,is_over,total) = contract.functions.getBetTotalOdds(bet_id).call({'from': cbet_account_owner_addr})
   (addr,bet_amount,is_ether) = contract.functions.getBetTotalBet(bet_id).call({'from': cbet_account_owner_addr})
   st.write(f"sportbook: {sportbook}")
   st.write(f"gameStatus: {gameStatus}")
   st.write(f"team: {team}")
   st.write(f"odds: {odds}")
   st.write(f"is_over: {str(is_over)}")
   st.write(f"total: {total}")
   st.write(f"addr: {addr}")
   st.write(f"bet_amount: {bet_amount/WEI_FACTOR}")
   st.write(f"is_ether: {str(is_ether)}")

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))

   st.write("Done")

if st.button("Place Bet #4, Moneyline, 1 Cbet"):
   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   bet_id = 1 
   sportbook = "FanDuel" 
   team = "Philadelphia Eagles"
   odds = -156
   addr = user_address
   bet_amount = (1 * WEI_FACTOR)
   is_ether = False
   
   contract.functions.createMoneylineBet(bet_id,sportbook,team,odds,addr,bet_amount,is_ether).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   
   st.write(f"BetType: {contract.functions.getBetType(bet_id).call({'from': cbet_account_owner_addr})}")
   (sportbook,gameStatus,team,odds) = contract.functions.getBetMoneyLineOdds(bet_id).call({'from': cbet_account_owner_addr})
   (addr,bet_amount,is_ether) = contract.functions.getBetMoneyLineBet(bet_id).call({'from': cbet_account_owner_addr})
   st.write(f"sportbook: {sportbook}")
   st.write(f"gameStatus: {gameStatus}")
   st.write(f"team: {team}")
   st.write(f"odds: {odds}")
   st.write(f"addr: {addr}")
   st.write(f"bet_amount: {bet_amount/WEI_FACTOR}")
   st.write(f"is_ether: {str(is_ether)}")

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))

   st.write("Done")

if st.button("Place Bet #5, Spread, 1 Cbet"):
   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())


   bet_id = 1 
   sportbook = "FanDuel" 
   team = "San Fransisco"
   odds = 100
   spread = int((2.5 * SPREAD_FACTOR))
   addr = user_address
   bet_amount = (1 * WEI_FACTOR)
   is_ether = False
   
   contract.functions.createSpreadBet(bet_id,sportbook,team,odds,spread,addr,bet_amount,is_ether).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   
   st.write(f"BetType: {contract.functions.getBetType(bet_id).call({'from': cbet_account_owner_addr})}")
   (sportbook,gameStatus,team,odds,spread) = contract.functions.getBetSpreadOdds(bet_id).call({'from': cbet_account_owner_addr})
   (addr,bet_amount,is_ether) = contract.functions.getBetSpreadBet(bet_id).call({'from': cbet_account_owner_addr})
   st.write(f"sportbook: {sportbook}")
   st.write(f"gameStatus: {gameStatus}")
   st.write(f"team: {team}")
   st.write(f"odds: {odds}")
   st.write(f"spread: {spread}")
   st.write(f"addr: {addr}")
   st.write(f"bet_amount: {bet_amount/WEI_FACTOR}")
   st.write(f"is_ether: {str(is_ether)}")

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))

   st.write("Done")

if st.button("Place Bet #6, Total, 1 Cbet"):
   (user_balance_wallet_ether_before, user_balance_wallet_token_before) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_before, user_balance_betting_token_before) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_before, user_balance_escrow_token_before) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_before_internal, house_balance_betting_token_before) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_before, house_balance_escrow_token_before) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_before) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_before
   (balance_owner_ether_before, balance_owner_token_before) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())
 
   bet_id = 1 
   sportbook = "FanDuel" 
   team = "San Fransisco"
   odds = 100
   is_over = True
   total = int(46.5 * TOTAL_FACTOR)
   addr = user_address
   bet_amount = (1 * WEI_FACTOR)
   is_ether = False
   
   contract.functions.createTotalBet(bet_id,sportbook,team,odds,is_over,total,addr,bet_amount,is_ether).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   
   st.write(f"BetType: {contract.functions.getBetType(bet_id).call({'from': cbet_account_owner_addr})}")
   (sportbook,gameStatus,team,odds,is_over,total) = contract.functions.getBetTotalOdds(bet_id).call({'from': cbet_account_owner_addr})
   (addr,bet_amount,is_ether) = contract.functions.getBetTotalBet(bet_id).call({'from': cbet_account_owner_addr})
   st.write(f"sportbook: {sportbook}")
   st.write(f"gameStatus: {gameStatus}")
   st.write(f"team: {team}")
   st.write(f"odds: {odds}")
   st.write(f"is_over: {str(is_over)}")
   st.write(f"total: {total}")
   st.write(f"addr: {addr}")
   st.write(f"bet_amount: {bet_amount/WEI_FACTOR}")
   st.write(f"is_ether: {str(is_ether)}")

   (user_balance_wallet_ether_after, user_balance_wallet_token_after) = (w3.eth.getBalance(user_address), contract.functions.balanceCbetTokens(user_address).call())
   (user_balance_betting_ether_after, user_balance_betting_token_after) = contract.functions.getBalanceUserBetting(user_address).call()
   (user_balance_escrow_ether_after, user_balance_escrow_token_after) = contract.functions.getBalanceUserEscrow(user_address).call()
   (house_balance_betting_ether_after_internal, house_balance_betting_token_after) = contract.functions.getBalanceHouseBetting().call()
   (house_balance_escrow_ether_after, house_balance_escrow_token_after) = contract.functions.getBalanceHouseEscrow().call()
   (house_balance_betting_ether_after) = w3.eth.getBalance(cbet_account_betting_addr) - house_balance_escrow_ether_after
   (balance_owner_ether_after, balance_owner_token_after) = (w3.eth.getBalance(cbet_account_owner_addr), contract.functions.balanceCbetTokens(cbet_account_owner_addr).call())

   st.write("User Wallet Balance: " + str(user_balance_wallet_ether_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_ether_after/WEI_FACTOR) + " / " + str(user_balance_wallet_token_before/WEI_FACTOR) + "-->" + str(user_balance_wallet_token_after/WEI_FACTOR))
   st.write("User Betting Balance: " + str(user_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(user_balance_betting_ether_after/WEI_FACTOR) + " / " + str(user_balance_betting_token_before/WEI_FACTOR) + "-->" + str(user_balance_betting_token_after/WEI_FACTOR))
   st.write("User Escrow Balance: " + str(user_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(user_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(user_balance_escrow_token_after/WEI_FACTOR))
   st.write("House Betting Balance: " + str(house_balance_betting_ether_before/WEI_FACTOR) + "-->" + str(house_balance_betting_ether_after/WEI_FACTOR) + " / " + str(house_balance_betting_token_before/WEI_FACTOR) + "-->" + str(house_balance_betting_token_after/WEI_FACTOR))
   st.write("House Escrow Balance: " + str(house_balance_escrow_ether_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_ether_after/WEI_FACTOR) + " / " + str(house_balance_escrow_token_before/WEI_FACTOR) + "-->" + str(house_balance_escrow_token_after/WEI_FACTOR))
   st.write("Owner/Deployer Balance: " + str(balance_owner_ether_before/WEI_FACTOR) + "-->" + str(balance_owner_ether_after/WEI_FACTOR) + " / " + str(balance_owner_token_before/WEI_FACTOR) + "-->" + str(balance_owner_token_after/WEI_FACTOR))

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

