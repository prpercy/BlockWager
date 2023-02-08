import requests
import pandas as pd
from streamlit.components.v1 import html
import sqlalchemy as sql

games_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36',
    'Dnt': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en',
    'origin': 'http://stats.nba.com',
    'Referer': 'https://github.com'
}

data_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
    'Accept-Language': 'en-us',
    'Referer': 'https://stats.nba.com/teams/traditional/?sort=W_PCT&dir=-1&Season=2019-20&SeasonType=Regular%20Season',
    'Connection': 'keep-alive',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true'
}


def get_json_data(url):
    raw_data = requests.get(url, headers=data_headers)
    json = raw_data.json()
    return json.get('resultSets')


def get_todays_games_json(url):
    raw_data = requests.get(url, headers=games_header)
    json = raw_data.json()
    return json.get('gs').get('g')


def to_data_frame(data):
    data_list = data[0]
    return pd.DataFrame(data=data_list.get('rowSet'), columns=data_list.get('headers'))


def create_todays_games(input_list):
    games = []
    for game in input_list:
        home = game.get('h')
        away = game.get('v')
        home_team = home.get('tc') + ' ' + home.get('tn')
        away_team = away.get('tc') + ' ' + away.get('tn')
        games.append([home_team, away_team])
    return games


def create_todays_games_from_odds(input_dict):
    games = []
    for game in input_dict.keys():
        home_team, away_team = game.split(":")
        games.append([home_team, away_team])
    return games


def payout(stake, odds):
    if odds > 0:
        return (stake * (odds / 100)) + stake
    else:
        return abs((stake / (odds / 100))) + stake
    

# create database engine
def get_db_engine():
    # Create a database connection string
    db_connection_string = 'sqlite:///./resources/app.db'
    
    # Create a database engine
    db_engine = sql.create_engine(db_connection_string)
    
    return db_engine

# initiate database tables
def initiate_database_tables(db_engine):
        
    create_bet_table = """
        CREATE TABLE bet (
            bet_id INT IDENTITY(1,1) PRIMARY KEY,
            sportsbook VAR,
            game VAR,
            team VAR,
            bet_type VAR,
            odds DOUBLE,
            amount DOUBLE,
            spread DOUBLE,
            total DOUBLE,
            isOver INT,
            isEther INT,
            status VAR,
            payout DOUBLE,
            user_account_Addr VAR
        )
        """
    db_engine.execute(create_bet_table)
        
    return True

# function to insert bet details into database
def create_bet(bet_id, bet, user_account_Addr, db_engine):
    
    bet_query = f"""
    INSERT INTO 
        bet (bet_id, sportsbook, game, team, bet_type, odds, amount, spread, total, isOver, isEther, user_account_Addr)
    VALUES 
        ('{bet_id}', '{bet.sportsbook}', '{bet.game}', '{bet.team}', '{bet.bet_type}', {bet.odds}, {bet.amount}, {bet.spread}, {bet.total}, {int(bet.isOver)}, {int(bet.isEther)}, '{user_account_Addr}')
    """
    db_engine.execute(bet_query)
      
    return bet

def update_bet_status_payout(bet_id, payout, status, db_engine):
    
    bet_status_update_query = f"""
    UPDATE bet 
    SET status = '{status}', payout = '{payout}'
    WHERE bet_id ='{bet_id}'
    """
    db_engine.execute(bet_status_update_query)
    
    return True

def retrieve_user_bets(user_account_Addr, db_engine):
    retrieve_user_bets_query = f"""
    SELECT 
        bet_id, sportsbook, game, team, bet_type, odds, amount, spread, total, isOver, isEther, status, payout, user_account_Addr 
    FROM 
        bet 
    WHERE user_account_Addr = '{user_account_Addr}' and bet_type = 'Spread'
    """
    
    bet_results_spread_cur = db_engine.execute(retrieve_user_bets_query)
    
    bet_results_spread = [r for r in bet_results_spread_cur]
    
    retrieve_user_bets_query = f"""
    SELECT 
        bet_id, sportsbook, game, team, bet_type, odds, amount, spread, total, isOver, isEther, status, payout, user_account_Addr 
    FROM 
        bet 
    WHERE user_account_Addr = '{user_account_Addr}' and bet_type = 'Total'
    """
    
    bet_results_total_cur = db_engine.execute(retrieve_user_bets_query)
    bet_results_total = [r for r in bet_results_total_cur]
 
    retrieve_user_bets_query = f"""
    SELECT 
        bet_id, sportsbook, game, team, bet_type, odds, amount, spread, total, isOver, isEther, status, payout, user_account_Addr 
    FROM 
        bet 
    WHERE user_account_Addr = '{user_account_Addr}' and bet_type = 'ML'
    """
    
    bet_results_ml_cur = db_engine.execute(retrieve_user_bets_query)
    bet_results_ml = [r for r in bet_results_ml_cur]
    
    bet_results = {
        'ML' : bet_results_ml,
        'Spread' : bet_results_spread,
        'Total' : bet_results_total
    }
    
    return bet_results


def get_bet_id_counter(db_engine):
    get_bet_id_counter = f"""
    SELECT 
        COUNT(*)
    FROM 
        bet 
    """
    
    result = db_engine.scalar(get_bet_id_counter)+1

    return result

# to navigate in streamlit app from one page to another
def nav_page(page_name, timeout_secs=5):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)