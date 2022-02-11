import sys
sys.path.append("..") 

from command_parser import parse_get_event
from tinydb import Query
from pretty_print import pretty_print_results

async def run_get_event_by_name(message, match_db):
  not_well_formed_command = 'No event was supplied or the command was not well formed.\nThe format for this command is `$get_event "event"`'
  try:
    event = parse_get_event(message.content, '$get_event')
  except:
    await message.channel.send(not_well_formed_command)
    return 
  if event is None:
    await message.channel.send(not_well_formed_command)
    return

  query_obj = Query()

  def find_event_func(matches):
    result = list(filter(lambda match: match['event'] == event, matches))
    return len(result) != 0

  needle = match_db.search(
    query_obj.matches_data.test(find_event_func)
  )
  # the search option is not that robust and returns the whole dictionary
  # So we need to flatten out the list of dicts
  flattened_results_list = []
  for sublist in needle:
      for match in sublist['matches_data']:
          if match['event'] == event:
            flattened_results_list.append(match)

 
  if len(flattened_results_list) == 0:
    await message.channel.send(
      'No results found for event: `{0}`'.format(event)
      )
  else:
    result = map(pretty_print_results, flattened_results_list)
    for val in result:
      await message.channel.send(
        'Results: {0}'.format(val)
        )  