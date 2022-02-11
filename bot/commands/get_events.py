import sys
sys.path.append("..") 

from database_methods import get_all_events

def run_get_events():
  events = get_all_events()

  result = "\n\t".join(events)
  return {'result' : 'All Events:\n\t{0}'.format(result)}
