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
cbet_account_wallet_addr = accounts[1]
bettor_accountr_addr_1 = accounts[2]
bettor_accountr_addr_2 = accounts[3]
bettor_accountr_addr_3 = accounts[4]

st.write("(1st Ganache Acct) ---> cbet_account_owner_addr=" + cbet_account_owner_addr)
st.write("(2nd Ganache Acct) ---> cbet_account_wallet_addr=" + cbet_account_wallet_addr)
st.write("(3rd Ganache Acct) ---> bettor_accountr_addr_1=" + bettor_accountr_addr_1)
st.write("(4th Ganache Acct) ---> bettor_accountr_addr_2=" + bettor_accountr_addr_2)
st.write("(5th Ganache Acct) ---> bettor_accountr_addr_3" + bettor_accountr_addr_3)
st.write("---")

#################################################################################
## Set Sports Teams To Bet On
#################################################################################

st.write("Test setting sports to bet on....")

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

st.write("Test setting teams to bet on....")

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

st.write("Test setting teams to bet on....")

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

st.write("Test setting up user/bettor accounts....")

if st.button("Setup Cbet account wallet addr"):
   contract.functions.setCACbetAccountWalletAddr(cbet_account_wallet_addr).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.setBACbetAccountWalletAddr(cbet_account_wallet_addr).transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   st.write(cbet_account_wallet_addr)
   st.write("Done")

if st.button("Setup betc user/bettor account"):
   st.write(bettor_accountr_addr_1)
   st.write(bettor_accountr_addr_2)
   st.write(bettor_accountr_addr_3)

   contract.functions.createBettorAccount(bettor_accountr_addr_1, "FirstName1", "LastName1", "username1", "passowrd1").transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createBettorAccount(bettor_accountr_addr_2, "FirstName2", "LastName2", "username2", "passowrd2").transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   contract.functions.createBettorAccount(bettor_accountr_addr_3, "FirstName3", "LastName3", "username3", "passowrd3").transact({'from': cbet_account_owner_addr, 'gas': 1000000})
   
   (bettor_account_first_name_1, bettor_account_last_name_1) = contract.functions.getBettorAccountName(bettor_accountr_addr_1).call()
   (bettor_account_first_name_2, bettor_account_last_name_2) = contract.functions.getBettorAccountName(bettor_accountr_addr_2).call()
   (bettor_account_first_name_3, bettor_account_last_name_3) = contract.functions.getBettorAccountName(bettor_accountr_addr_3).call()

   st.write(bettor_account_first_name_1+" "+bettor_account_last_name_1)
   st.write(bettor_account_first_name_2+" "+bettor_account_last_name_2)
   st.write(bettor_account_first_name_3+" "+bettor_account_last_name_3)

   st.write("Done")

better_1_ether = st.text_input("Better1: Entery amount of ether to deposit into cbet account")
if st.button("Better1: Make deposit"):
   st.write(bettor_accountr_addr_1)
   
   contract.functions.depositBettorAccountEther().transact({'from': bettor_accountr_addr_1, "value": w3.toWei(better_1_ether, "ether"), 'gas': 1000000})
   better_1_cbet_accont_ether_balance = contract.functions.getBalanceBettorAccountEther().call({'from': bettor_accountr_addr_1})
   total_cbet_accont_ether_balance = contract.functions.getBalanceCbetAccountEther().call({'from': cbet_account_owner_addr})
   
   st.write("Better1 Ether Cbet Account Balance:"+str(better_1_cbet_accont_ether_balance))
   st.write("Ttoal Ether Cbet Account Balance:"+str(total_cbet_accont_ether_balance))      
   
   st.write("Done")

better_2_ether = st.text_input("Better2: Entery amount of ether to deposit into cbet account")
if st.button("Better2: Make deposit"):
   st.write(bettor_accountr_addr_2)
   
   contract.functions.depositBettorAccountEther().transact({'from': bettor_accountr_addr_2, "value": w3.toWei(better_2_ether, "ether"), 'gas': 1000000})
   better_2_cbet_accont_ether_balance = contract.functions.getBalanceBettorAccountEther().call({'from': bettor_accountr_addr_2})
   total_cbet_accont_ether_balance = contract.functions.getBalanceCbetAccountEther().call({'from': cbet_account_owner_addr})
   
   st.write("Better2 Ether Cbet Account Balance:"+str(better_2_cbet_accont_ether_balance))
   st.write("Ttoal Ether Cbet Account Balance:"+str(total_cbet_accont_ether_balance))      
   
   st.write("Done")

better_3_ether = st.text_input("Better3: Entery amount of ether to deposit into cbet account")
if st.button("Better3: Make deposit"):
   st.write(bettor_accountr_addr_3)
   
   contract.functions.depositBettorAccountEther().transact({'from': bettor_accountr_addr_3, "value": w3.toWei(better_3_ether, "ether"), 'gas': 1000000})
   better_3_cbet_accont_ether_balance = contract.functions.getBalanceBettorAccountEther().call({'from': bettor_accountr_addr_3})
   total_cbet_accont_ether_balance = contract.functions.getBalanceCbetAccountEther().call({'from': cbet_account_owner_addr})
   
   st.write("Better3 Ether Cbet Account Balance:"+str(better_3_cbet_accont_ether_balance))
   st.write("Ttoal Ether Cbet Account Balance:"+str(total_cbet_accont_ether_balance))      
   
   st.write("Done")

better_1_ether = st.text_input("Better1: Entery amount of ether to withdrawal into cbet account")
if st.button("Better1: Make withdrawal"):
   st.write(bettor_accountr_addr_1)
   
   contract.functions.withdrawBettorAccountEther(bettor_accountr_addr_1).transact({'from': cbet_account_wallet_addr, "value": w3.toWei(better_1_ether, "ether"), 'gas': 1000000})
   better_1_cbet_accont_ether_balance = contract.functions.getBalanceBettorAccountEther().call({'from': bettor_accountr_addr_1})
   total_cbet_accont_ether_balance = contract.functions.getBalanceCbetAccountEther().call({'from': cbet_account_owner_addr})
   
   st.write("Better1 Ether Cbet Account Balance:"+str(better_1_cbet_accont_ether_balance))
   st.write("Ttoal Ether Cbet Account Balance:"+str(total_cbet_accont_ether_balance))      
   
   st.write("Done")

better_2_ether = st.text_input("Better2: Entery amount of ether to withdrawal into cbet account")
if st.button("Better2: Make withdrawal"):
   st.write(bettor_accountr_addr_2)
   
   contract.functions.withdrawBettorAccountEther().transact({'from': bettor_accountr_addr_2, "value": w3.toWei(better_2_ether, "ether"), 'gas': 1000000})
   better_2_ether = contract.functions.getBalanceBettorAccountEther().call({'from': bettor_accountr_addr_2})
   total_cbet_accont_ether_balance = contract.functions.getBalanceCbetAccountEther().call({'from': cbet_account_owner_addr})
   
   st.write("Better2 Ether Cbet Account Balance:"+str(better_2_ether))
   st.write("Ttoal Ether Cbet Account Balance:"+str(total_cbet_accont_ether_balance))      
   
   st.write("Done")
   
better_3_ether = st.text_input("Better3: Entery amount of ether to withdrawal into cbet account")
if st.button("Better3: Make withdrawal"):
   st.write(bettor_accountr_addr_3)
   
   contract.functions.withdrawBettorAccountEther().transact({'from': bettor_accountr_addr_3, "value": w3.toWei(better_3_ether, "ether"), 'gas': 1000000})
   better_3_ether = contract.functions.getBalanceBettorAccountEther().call({'from': bettor_accountr_addr_3})
   total_cbet_accont_ether_balance = contract.functions.getBalanceCbetAccountEther().call({'from': cbet_account_owner_addr})
   
   st.write("Better3 Ether Cbet Account Balance:"+str(better_3_ether))
   st.write("Ttoal Ether Cbet Account Balance:"+str(total_cbet_accont_ether_balance))      
   
   st.write("Done")
      
# ToDo:
#  - Add comments
#  - Use SafeMath
#  - Add a bunch of require checks
#  - Decide what should or should not be public
#  - Look for ways to make gas more efficient
#  - On vs. Off chain distribution
#  - Owner cannot deposit into his own wallet (withdraw + deposit nto allowed)
#  - Owner cannot bet
#  - Set minimum bet requirement
#  - activate/deactivae account
#  - create separate balance for account balance versus escrow (bets in progress)
#  - if game has not started, able to remove funds from escrow back to account
#  - be able to withdrawal from account

