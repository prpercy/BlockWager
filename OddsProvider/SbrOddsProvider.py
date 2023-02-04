from sbrscrape import Scoreboard
from pprint import pprint
import inspect

class SbrOddsProvider:
    
    """ Abbreviations dictionary for team location which are sometimes saved with abbrev instead of full name. 
    Moneyline options name require always full name
    Returns:
        string: Full location name
    """    

    def __init__(self, sportsbook="fanduel"):
        self.games = Scoreboard(sport="NBA").games
        self.sportsbook = sportsbook
    
    def get_odds(self):
        """Function returning odds from Sbr server's json content

        Returns:
            dictionary: [home_team_name + ':' + away_team_name: { home_team: money_line_odds, away_team: money_line_odds }, under_over_odds: val]
        """
        dict_res = {}
        dict_games = {}
        idx = 1
        for game in self.games:
            # Get team names
            home_team_name = game['home_team'].replace("Los Angeles Clippers", "LA Clippers")
            away_team_name = game['away_team'].replace("Los Angeles Clippers", "LA Clippers")
            
            money_line_home_value = money_line_away_value = totals_value = None

            # Get money line bet values
            if self.sportsbook in game['home_ml']:
                money_line_home_value = game['home_ml'][self.sportsbook]
            if self.sportsbook in game['away_ml']:
                money_line_away_value = game['away_ml'][self.sportsbook]
                
                
            # Get spread values
            if self.sportsbook in game['home_spread']:
                spread_home_value = game['home_spread'][self.sportsbook]
            if self.sportsbook in game['away_spread']:
                spread_away_value = game['away_spread'][self.sportsbook]
            
            # Get totals bet value
            if self.sportsbook in game['total']:
                totals_value = game['total'][self.sportsbook]
            
            dict_games[idx] = {
                'game': home_team_name + '<>' + away_team_name, 
                'home_team': home_team_name, 'home_ml_odds': money_line_home_value, 'home_spread' : spread_home_value, 'home_total':totals_value,
                'away_team': away_team_name, 'away_ml_odds': money_line_away_value, 'away_spread' : spread_away_value, 'away_total':totals_value
            }
            dict_res[home_team_name + ':' + away_team_name] =  { 
                home_team_name: { 'money_line_odds': money_line_home_value, 'spread':spread_home_value, 'total': totals_value}, 
                away_team_name: { 'money_line_odds': money_line_away_value, 'spread':spread_away_value, 'total': totals_value }
            }
            idx = idx+1
        return dict_res, dict_games
    
    
   
##currently unimplemented function that attempts to do same thing as NBA Odds, but for the super bowl 
    def get_odds_nhl(self):
        dict_res_nhl = {}
        for game in self.games_nfl:
            # Get team names
            home_team_name = game['home_team'].replace("Philidelphia", "Phildelphia Eagles")
            away_team_name = game['away_team'].replace("Kansas City", "Kansas City Chiefs") 
            
            money_line_home_value = money_line_away_value = totals_value = None

            # Get money line bet values
            if self.sportsbook in game['home_ml']:
                money_line_home_value = game['home_ml'][self.sportsbook]
            if self.sportsbook in game['away_ml']:
                money_line_away_value = game['away_ml'][self.sportsbook]
            
            # Get totals bet value
            if self.sportsbook in game['total']:
                totals_value = game['total'][self.sportsbook]
            
            dict_res_nhl[home_team_name + ':' + away_team_name] =  { 
                'under_over_odds': totals_value,
                home_team_name: { 'money_line_odds': money_line_home_value }, 
                away_team_name: { 'money_line_odds': money_line_away_value }
            }
        return dict_res_nhl