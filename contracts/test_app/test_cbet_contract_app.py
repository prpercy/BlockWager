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
cbet_account_owner_addr = accounts[0]
cbet_account_betting_addr = accounts[1]
user_account_addr_1 = accounts[2]
user_account_addr_2 = accounts[3]
user_account_addr_3 = accounts[4]

st.write("(1st Ganache Acct) ---> cbet_account_owner_addr=" + cbet_account_owner_addr)
st.write("(2nd Ganache Acct) ---> cbet_account_betting_addr=" + cbet_account_betting_addr)
st.write("(3rd Ganache Acct) ---> user_account_addr_1=" + user_account_addr_1)
st.write("(4th Ganache Acct) ---> user_account_addr_2=" + user_account_addr_2)
st.write("(5th Ganache Acct) ---> user_account_addr_3" + user_account_addr_3)
st.write("---")

WEI_FACTOR = 1000000000000000000

#################################################################################
## Set Sports Teams To Bet On
#################################################################################

st.write("TEST SETTING SPORTS TO BET ON")

sports_str_lst = ["NFL", "NBA", "MLB", "NHL", "MLS", "Cricket"]
sports_id_lst = [1, 2, 3, 4, 5, 6]

if st.button("Test create sports"):
   contract.functions.createSport(sports_str_lst[0]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createSport(sports_str_lst[1]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createSport(sports_str_lst[2]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createSport(sports_str_lst[3]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createSport(sports_str_lst[4]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createSport(sports_str_lst[5]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   st.write("Done!")

if st.button("Test getting sports names"):
   st.write(contract.functions.getSportName(sports_id_lst[0]).call())
   st.write(contract.functions.getSportName(sports_id_lst[1]).call())
   st.write(contract.functions.getSportName(sports_id_lst[2]).call())
   st.write(contract.functions.getSportName(sports_id_lst[3]).call())
   st.write(contract.functions.getSportName(sports_id_lst[4]).call())
   st.write(contract.functions.getSportName(sports_id_lst[5]).call())  
   st.write("Done!")
   
if st.button("Test getting sports ids"):
   st.write(str(contract.functions.getSportId(sports_str_lst[0]).call()))
   st.write(str(contract.functions.getSportId(sports_str_lst[1]).call()))
   st.write(str(contract.functions.getSportId(sports_str_lst[2]).call()))
   st.write(str(contract.functions.getSportId(sports_str_lst[3]).call()))
   st.write(str(contract.functions.getSportId(sports_str_lst[4]).call()))
   st.write(str(contract.functions.getSportId(sports_str_lst[5]).call())) 
   st.write("Done!")

st.write("---")

st.write("TEST SETTING TEAMS TO BET ON")

teams_str_lst = ["San Francisco 49ers", "Philadelphia Eagles", "Cincinatti Bengals", "Kansas City Chiefs", "New York Rangers", "New York Islanders", "New York Knicks", "New Jersey Nets", "India", "South Africa"]
teams_id_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

if st.button("Test create teams"):
   contract.functions.createTeam(teams_str_lst[0]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createTeam(teams_str_lst[1]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createTeam(teams_str_lst[2]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createTeam(teams_str_lst[3]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createTeam(teams_str_lst[4]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createTeam(teams_str_lst[5]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createTeam(teams_str_lst[6]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createTeam(teams_str_lst[7]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createTeam(teams_str_lst[8]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createTeam(teams_str_lst[9]).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   st.write("Done!")

if st.button("Test getting teams names"):
   st.write(contract.functions.getTeamName(teams_id_lst[0]).call())
   st.write(contract.functions.getTeamName(teams_id_lst[1]).call())
   st.write(contract.functions.getTeamName(teams_id_lst[2]).call())
   st.write(contract.functions.getTeamName(teams_id_lst[3]).call())
   st.write(contract.functions.getTeamName(teams_id_lst[4]).call())
   st.write(contract.functions.getTeamName(teams_id_lst[5]).call())  
   st.write(contract.functions.getTeamName(teams_id_lst[6]).call())  
   st.write(contract.functions.getTeamName(teams_id_lst[7]).call())  
   st.write(contract.functions.getTeamName(teams_id_lst[8]).call())  
   st.write(contract.functions.getTeamName(teams_id_lst[9]).call())  
   st.write("Done!")
   
if st.button("Test getting teams ids"):
   st.write(str(contract.functions.getTeamId(teams_str_lst[0]).call()))
   st.write(str(contract.functions.getTeamId(teams_str_lst[1]).call()))
   st.write(str(contract.functions.getTeamId(teams_str_lst[2]).call()))
   st.write(str(contract.functions.getTeamId(teams_str_lst[3]).call()))
   st.write(str(contract.functions.getTeamId(teams_str_lst[4]).call()))
   st.write(str(contract.functions.getTeamId(teams_str_lst[5]).call())) 
   st.write(str(contract.functions.getTeamId(teams_str_lst[6]).call())) 
   st.write(str(contract.functions.getTeamId(teams_str_lst[7]).call())) 
   st.write(str(contract.functions.getTeamId(teams_str_lst[8]).call())) 
   st.write(str(contract.functions.getTeamId(teams_str_lst[9]).call())) 
   st.write("Done!")

st.write("---")

st.write("TEST SETTING GAMES TO BET ON")

SPREAD_FACTOR = 100
OVERUNDER_FACTOR = 1000
WEI_FACTOR = 1000000000000000000

if st.button("Test setting up game 1"):
   sport_id = 1
   away_team = "San Francisco 49ers"
   home_team = "Philadelphia Eagles"
   away_team_odss_moneyline = 132
   home_team_odss_moneyline = -156
   away_team_odds_spread = -100
   home_team_odds_spread = -122
   home_spread = int(-2.5 * SPREAD_FACTOR)
   away_spread = int(2.5 * SPREAD_FACTOR)
   away_team_odds_overunder = -102
   home_team_odds_overunder = -120
   overunder = int(46.5*OVERUNDER_FACTOR)

   away_team_id = contract.functions.getTeamId(away_team).call()
   home_team_id = contract.functions.getTeamId(home_team).call()
   
   contract.functions.createGame(sport_id, home_team_id, away_team_id, 
                                 home_team_odss_moneyline, away_team_odss_moneyline,
                                 home_team_odds_spread, away_team_odds_spread, home_spread, away_spread,
                                 home_team_odds_overunder, away_team_odds_overunder, overunder).transact({'from': cbet_account_owner_addr, 'gas': 1000000})      
   game_1_id = contract.functions.getLastGameId().call()
   
   (home_team_id,away_team_id) = contract.functions.getGameTeamIds(game_1_id).call()
   (home_team_odss_moneyline,away_team_odss_moneyline) = contract.functions.getGameMoneylineOdds(game_1_id).call()
   (home_team_odds_spread,away_team_odds_spread,home_spread,away_spread) = contract.functions.getGameSpreadOdds(game_1_id).call()
   (home_team_odds_overunder,away_team_odds_overunder,overunder) = contract.functions.getGameOverUnderOdds(game_1_id).call()

   sport_name = contract.functions.getSportName(sport_id).call()
   home_team = contract.functions.getTeamName(home_team_id).call()
   away_team = contract.functions.getTeamName(away_team_id).call()
   
   st.write("Sport:"+sport_name)
   st.write("Home team:"+home_team)
   st.write("Away team:"+away_team)
   st.write("Home team odds moneyline:"+str(home_team_odss_moneyline))
   st.write("Away team odds moneyline:"+str(away_team_odss_moneyline))
   st.write("Home team odds spread:"+str(home_team_odds_spread))
   st.write("Away team odds spread:"+str(away_team_odds_spread))
   st.write("Home Spread:"+str(float(home_spread/SPREAD_FACTOR)))
   st.write("Away Spread:"+str(float(away_spread/SPREAD_FACTOR)))
   st.write("Home team OverUnder:"+str(home_team_odds_overunder))
   st.write("Away team OverUnder:"+str(away_team_odds_overunder))
   st.write("OverUnder:"+str(float(overunder/OVERUNDER_FACTOR)))
   
   st.write("Done!")

if st.button("Test setting up game 2"):
   sport_id = 1
   away_team = "Cincinatti Bengals"
   home_team = "Kansas City Chiefs"
   away_team_odss_moneyline = 106
   home_team_odss_moneyline = -124
   away_team_odds_spread = -108
   home_team_odds_spread = -112
   home_spread = int(-1.5 * SPREAD_FACTOR)
   away_spread = int(1.5 * SPREAD_FACTOR)
   away_team_odds_overunder = -105
   home_team_odds_overunder = -115
   overunder = int(48.5*OVERUNDER_FACTOR)

   away_team_id = contract.functions.getTeamId(away_team).call()
   home_team_id = contract.functions.getTeamId(home_team).call()
   
   contract.functions.createGame(sport_id,home_team_id, away_team_id, 
                                 home_team_odss_moneyline, away_team_odss_moneyline,
                                 home_team_odds_spread, away_team_odds_spread, home_spread, away_spread,
                                 home_team_odds_overunder, away_team_odds_overunder, overunder).transact({'from': cbet_account_owner_addr, 'gas': 1000000})      
   game_2_id = contract.functions.getLastGameId().call()
   
   (home_team_id,away_team_id) = contract.functions.getGameTeamIds(game_2_id).call()
   (home_team_odss_moneyline,away_team_odss_moneyline) = contract.functions.getGameMoneylineOdds(game_2_id).call()
   (home_team_odds_spread,away_team_odds_spread,home_spread,away_spread) = contract.functions.getGameSpreadOdds(game_2_id).call()
   (home_team_odds_overunder,away_team_odds_overunder,overunder) = contract.functions.getGameOverUnderOdds(game_2_id).call()

   sport_name = contract.functions.getSportName(sport_id).call()
   home_team = contract.functions.getTeamName(home_team_id).call()
   away_team = contract.functions.getTeamName(away_team_id).call()
   
   st.write("Sport:"+sport_name)
   st.write("Home team:"+home_team)
   st.write("Away team:"+away_team)
   st.write("Home team odds moneyline:"+str(home_team_odss_moneyline))
   st.write("Away team odds moneyline:"+str(away_team_odss_moneyline))
   st.write("Home team odds spread:"+str(home_team_odds_spread))
   st.write("Away team odds spread:"+str(away_team_odds_spread))
   st.write("Home Spread:"+str(float(home_spread/SPREAD_FACTOR)))
   st.write("Away Spread:"+str(float(away_spread/SPREAD_FACTOR)))
   st.write("Home team OverUnder:"+str(home_team_odds_overunder))
   st.write("Away team OverUnder:"+str(away_team_odds_overunder))
   st.write("OverUnder:"+str(float(overunder/OVERUNDER_FACTOR)))
   
   st.write("Done!")

st.write("---")

st.write("TEST SETTING UP USER ACCOUNTS")

if st.button("Setup user account"):
   st.write(user_account_addr_1)
   st.write(user_account_addr_2)
   st.write(user_account_addr_3)

   contract.functions.createUserAccount(user_account_addr_1, "FirstName1", "LastName1", "username1", "passowrd1").transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createUserAccount(user_account_addr_2, "FirstName2", "LastName2", "username2", "passowrd2").transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createUserAccount(user_account_addr_3, "FirstName3", "LastName3", "username3", "passowrd3").transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   
   (user_account_first_name_1, user_account_last_name_1) = contract.functions.getUserAccountName(user_account_addr_1).call()
   (user_account_first_name_2, user_account_last_name_2) = contract.functions.getUserAccountName(user_account_addr_2).call()
   (user_account_first_name_3, user_account_last_name_3) = contract.functions.getUserAccountName(user_account_addr_3).call()

   st.write(user_account_first_name_1+" "+user_account_last_name_1)
   st.write(user_account_first_name_2+" "+user_account_last_name_2)
   st.write(user_account_first_name_3+" "+user_account_last_name_3)

   st.write("Done")

if st.button("Setup betting account"):
   st.write("cbet_account_betting_addr="+cbet_account_betting_addr)
   contract.functions.setCbetBettingAddr(cbet_account_betting_addr).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   st.write("Total Ether Betting Balance:"+str(w3.eth.getBalance(cbet_account_betting_addr)/WEI_FACTOR))
      
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

