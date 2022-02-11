import sys
sys.path.append("..") 

from database_methods import get_all_players

def run_get_players():
  players = get_all_players()

  result = "\n\t".join(players)

  return {'result' : 'All Players:\n\t{0}'.format(result) }  
