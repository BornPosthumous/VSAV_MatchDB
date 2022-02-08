import shlex
from command_parser import(
  parse_command, 
  parse_db_item, 
  parse_matchup_command,
  parse_get_event,
  parse_get_matches_from_video
)
from pretty_print import pretty_print_results
from validators import(
  is_valid_character, 
  all_valid, 
  validate_match,
  validate_url,
)
from tinydb import Query, TinyDB

def get_db():
  db = TinyDB('./matchDB.json')
  return(db)


async def run_get_valid_character_names(message):
    await message.channel.send('Valid Character names are as follows:\n```{0}```'.format( all_valid))
    return   

async def run_get_events(message, match_db):
  events = []

  for item in match_db:
    for match in item['matches_data']:
      if match['event'] not in events:
        events.append(match['event'])

  result = "\n\t".join(events)
  await message.channel.send(
    'All Events:\n\t{0}'.format(result)
    )  

async def run_get_players(message, match_db):
  players = []

  for item in match_db:
    for match in item['matches_data']:
      if match['player_1'] not in players:
        players.append(match['player_1'])
      if match['player_2'] not in players:
        players.append(match['player_2'])

  result = "\n\t".join(players)
  await message.channel.send(
    'All Players:\n\t{0}'.format(result)
    )  

async def run_get_matches_from_video(message, match_db):
  not_well_formed_command = 'No video url was supplied or the command was not well formed.\nThe format for this command is `$get_matches_from_video "video url"`'
  try:
    url = parse_get_matches_from_video(message.content, '$get_matches_from_video')
  except:
    await message.channel.send(not_well_formed_command)
    return 
  if url is None:
    await message.channel.send(not_well_formed_command)
    return
  
  if not validate_url(url):
    await message.channel.send('The supplied url was not a valid Youtube video.')
    return
  
  query_obj = Query()

  def find_video_func(matches):
    result = list(filter(lambda match: match['url'] == url, matches))
    return len(result) != 0

  needle = match_db.search(
    query_obj.matches_data.test(find_video_func)
  )
  # the search option is not that robust and returns the whole dictionary
  # So we need to flatten out the list of dicts
  flattened_results_list = []
  for sublist in needle:
      for match in sublist['matches_data']:
          if match['url'] == url:
            flattened_results_list.append(match)

 
  if len(flattened_results_list) == 0:
    await message.channel.send(
      'No results found for video with url: `{0}`'.format(url)
      )
  else:
    result = map(pretty_print_results, flattened_results_list)
    for val in result:
      await message.channel.send(
        'Results: {0}'.format(val)
        )  

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

async def run_get_matchup(message, match_db):
  not_well_formed_command = 'No characters were supplied or the command was not well formed.\nThe format for this command is `$get_matchup "character name" vs "character name"`\nFor a list of valid characters, please run the following command: `$get_valid_character_names`'
  # to do list all valid char strings
    
  try:
    arguments = parse_matchup_command(message.content, '$get_matchup')
  except:
    await message.channel.send(not_well_formed_command)
    return 

  char_1 = arguments.get('char_1', None)
  char_2 = arguments.get('char_2', None)
  if not char_1 or not char_2:
    await message.channel.send(not_well_formed_command)
    return 

  query_obj = Query()

  def find_char_func(matches):
    result = list(
        filter(lambda match: (match['char_1'] == char_1 and match['char_2'] == char_2) or (match['char_2'] == char_1 and match['char_1'] == char_2 ) , matches)
    )
    return len(result) != 0


  needle = match_db.search(
    query_obj.matches_data.test(find_char_func)
  )
  # the search option is not that robust and returns the whole dictionary
  # So we need to flatten out the list of dicts
  flattened_results_list = []
  for sublist in needle:
      for match in sublist['matches_data']:
          if (match['char_1'] == char_1 and match['char_2'] == char_2) or (match['char_2'] == char_1 and match['char_1'] == char_2 ):
            flattened_results_list.append(match)

 
  if len(flattened_results_list) == 0:
    await message.channel.send(
      'No results found for `{0}` vs `{1}`'.format(char_1, char_2)
      )
  else:
    result = map(pretty_print_results, flattened_results_list)
    for val in result:
      await message.channel.send(
        'Results: {0}'.format(val)
        )  
async def run_get_character_matches(message, match_db):
  not_well_formed_command = 'No character was supplied or the command was not well formed.\nThe format for this command is `$get_character_matches "character"`\nFor a list of valid characters, please run the following command: `$get_valid_character_names`'
  # to do list all valid char strings
  try:
    split_message = message.content.replace('$get_character_matches', '')
    split_message = shlex.split(split_message)
    character = split_message[0]
    if character is None:
      await message.channel.send(not_well_formed_command)
      return 
  except:
      await message.channel.send(not_well_formed_command)
      return 
  parsed_character = is_valid_character(character)
  if parsed_character is None:
    await message.channel.send('`{0}` is not a valid character.\nFor a list of valid characters, please run the following command: `$get_valid_character_names`'.format(character, all_valid))
    return 

  query_obj = Query()

  def find_char_func(matches):
    result = list(
        filter(lambda match: match['char_1'] == parsed_character or match['char_2'] == parsed_character, matches)
    )
    return len(result) != 0


  needle = match_db.search(
    query_obj.matches_data.test(find_char_func)
  )
  # the search option is not that robust and returns the whole dictionary
  # So we need to flatten out the list of dicts
  flattened_results_list = []
  for sublist in needle:
      for match in sublist['matches_data']:
          if match['char_1'] == parsed_character or match['char_2'] == parsed_character:
            flattened_results_list.append(match)

 
  if len(flattened_results_list) == 0:
    await message.channel.send(
      'No results found for character `{0}`'.format(parsed_character)
      )
  else:
    result = map(pretty_print_results, flattened_results_list)
    for val in result:
      await message.channel.send(
        'Results: {0}'.format(val)
        )


async def run_get_player_matches(message, match_db):
  not_well_formed_command = 'No character was supplied or the command was not well formed \nThe format for this command is `$get_player_matches "player name"`'
  # to do list all valid char strings

  try:
    split_message = message.content.replace('$get_player_matches', '')
    split_message = shlex.split(split_message)
    player = split_message[0]
  except:
    await message.channel.send(not_well_formed_command)
    return 

  if player is None:
  
    await message.channel.send(not_well_formed_command)
    return 
  
  query_obj = Query()
  def find_player_func(matches):
    result = list(
        filter(lambda match: match['player_1'] == player or match['player_2'] == player, matches)
    )
    return len(result) != 0


  needle = match_db.search(
    query_obj.matches_data.test(find_player_func)
  )
  # the search option is not that robust and returns the whole dictionary
  # So we need to flatten out the list of dicts
  flattened_results_list = []
  for sublist in needle:
      for match in sublist['matches_data']:
          if match['player_1'] == player or match['player_2'] == player:
            flattened_results_list.append(match)
  
  if len(flattened_results_list) == 0:
    await message.channel.send(
      'No results found for player `{0}`'.format(player)
      )
  else:
    result = map(pretty_print_results, flattened_results_list)
    for val in result:
      await message.channel.send(
        'Results: {0}'.format(val)
        )

async def run_add_video(message, match_db):
  good_command = '$add_video url="https://www.youtube.com/watch?v=agoodvideo" player_1="playername1" char_1="character name p1" player_2="playername2" char_2="character name p2" winner="winning characters name" timestamp="timestamp in seconds"'
  valid_chars_help = "For a list of valid characters, please run the following command: `$get_valid_character_names`"

  arguments = parse_command(message.content, '$add_video')
  db_item = parse_db_item(arguments)

  if not validate_url(db_item['url']):
      await message.channel.send('The supplied url was not a valid Youtube video.')
      return
  # handle error
  if isinstance(db_item, str):
      await message.channel.send( 'Result: {0}'.format(db_item))
      return 

  missing = validate_match(db_item)

  if len(missing) != 0:
      parsed_missing = ' , '.join([str(elem) for elem in missing]) 
      error_msg = "Cannot add to DB, the following required fields were missing : " + parsed_missing

      await message.channel.send('Error: `{0}`\n\nFor reference here is the valid command format, you may use it as a template:\n`{1}`\n\n{2}\n'.format(
        error_msg, 
        good_command, 
        valid_chars_help
      ))
      return
  else:
    query_obj = Query()
    needle = match_db.search(query_obj.url == db_item['url'])

    if len(needle) != 0:
      add_tag_command = '$add_tag_to_video url="{0}" player_1="{1}" char_1="{2}" player_2="{3}" char_2="{4}" winner="{5}" timestamp="{6}" event="{7}" description="{8}"'.format(
        db_item['url'],
        db_item['player_1'],
        db_item['char_1'],
        db_item['player_2'],
        db_item['char_2'],
        db_item['winner'],
        db_item['timestamp'],
        db_item['event'],
        db_item['description'],
        )
      list_video_command = '$get_matches_from_video "{0}"'.format(db_item['url'])
      await message.channel.send(
        'Video already exists, please look through the current video tags with the following command:\n`{0}`\nIf you do not see the match you would like to tag add a tag to the video with the following command:\n`{1}`'.format(list_video_command, add_tag_command)
        )
      return

    match_db.insert({'url':db_item['url'], 'matches_data': [db_item]})
    await message.channel.send(
      'Your video has been added to the match database. Thank you for your contribution!!'
      )
    return


async def run_add_tag_to_video(message, match_db):
    good_command = '$add_tag_to_video url="https://www.youtube.com/watch?v=agoodvideo" player_1="playername1" char_1="character name p1" player_2="playername2" char_2="character name p2" winner="winning characters name" timestamp="timestamp in seconds"'
    valid_chars_help = "For a list of valid characters, please run the following command: `$get_valid_character_names`"

    try:
     arguments = parse_command(message.content, '$add_tag_to_video')
    except ValueError as e:
      await message.channel.send('The supplied command was not valid`{0}`\n For reference here is the valid commands format, you may use it as a template:\n`{1}`\n For a list of valid characters use the following command:\n`{2}`\n'.format(str(e)), good_command , valid_chars_help)
      return

    db_item = parse_db_item(arguments)

    if not validate_url(db_item['url']):
      await message.channel.send('The supplied url was not a valid Youtube video.')
      return

    missing = validate_match(db_item)

    if len(missing) != 0:
        parsed_missing = ' , '.join([str(elem) for elem in missing]) 
        error_msg = "Cannot add to DB, the following required fields were missing : " + parsed_missing

        await message.channel.send('Error: `{0}`\n\nFor reference here is the valid command format, you may use it as a template:\n`{1}`\n\n{2}\n'.format(
          error_msg, 
          good_command, 
          valid_chars_help
        ))
        return

    query_obj = Query()
    needle = match_db.search(query_obj.url == db_item['url'])
 
    if len(needle) == 0:
      add_video_command = '$add_video url="{0}" player_1="{1}" char_1="{2}" player_2="{3}" char_2="{4}" winner="{5}" timestamp="{6}" event="{7}" description="{8}"'.format(
        db_item['url'],
        db_item['player_1'],
        db_item['char_1'],
        db_item['player_2'],
        db_item['char_2'],
        db_item['winner'],
        db_item['timestamp'],
        db_item['event'],
        db_item['description'],
        )
      await message.channel.send(
        'Video does not exist, please add a video with the following command:\n`{0}`'.format(add_video_command)
        )
      return

    else:
      current_db_item = needle[0]
      _current_matches = current_db_item['matches_data']
      _current_matches.append(db_item)
      current_db_item["matches_data"] = _current_matches
      match_db.update(current_db_item, query_obj.url == db_item['url'])
      await message.channel.send(
        'Tagged matches for`{0}` have been updated.\nHere are all of the current tags for this video:\n\n'.format(db_item['url'])
      )
      flattened_results_list = []
      for match in current_db_item['matches_data']:
            flattened_results_list.append(match)
      
      result = map(pretty_print_results, flattened_results_list)
      for val in result:
        await message.channel.send(
          '{0}'.format(val)
          )  


async def remove_tag_from_video(message, match_db):
    good_command = '$remove_tag_from_video url="https://www.youtube.com/watch?v=agoodvideo" timestamp="timestamp in seconds"'
    add_video_command = '$add_video url="https://www.youtube.com/watch?v=agoodvideo" player_1="playername1" char_1="character name p1" player_2="playername2" char_2="character name p2" winner="winning characters name" timestamp="timestamp in seconds"'

    try:
     arguments = parse_command(message.content, '$remove_tag_from_video')
    except ValueError as e:
      not_well_formed_command = 'The supplied command was not a valid Youtube video: `{0}`\n For reference here is the valid commands format, you may use it as a template:\n`{1}`\n'.format(
        str(e), 
        good_command
      ) 
      await message.channel.send(not_well_formed_command)
      return

    try:
      db_item = parse_db_item(arguments)
    except:
      not_well_formed_command = 'The supplied command was not valid.\nFor reference here is the valid commands format, you may use it as a template:\n`{0}`\n'.format(good_command) 
      await message.channel.send(not_well_formed_command)
      return
    if not validate_url(db_item['url']):
      await message.channel.send('The supplied url was not a valid Youtube video.')
      return
    
    if not db_item['timestamp']:
      await message.channel.send('The supplied timestamp was not a number or was missing.\nTimestamps must be a number in seconds e.g. "100"'.format(db_item['timestamp']))
      return

    query_obj = Query()
    needle = match_db.search(query_obj.url == db_item['url'])
 
    if len(needle) == 0:
      await message.channel.send(
        'Video does not exist, please add a video with the following command:\n`{0}`'.format(add_video_command)
        )
      return

    else:
      current_db_item = needle[0]
      _current_matches = current_db_item['matches_data']
      matches_to_keep = []
      for match in _current_matches:
        if not (match['timestamp'] == db_item['timestamp']):
          matches_to_keep.append(match)

      current_db_item["matches_data"] = matches_to_keep
      match_db.update(current_db_item, query_obj.url == db_item['url'])
      await message.channel.send(
        'Tagged matches for`{0}` have been updated.\nHere are all of the current tags for this video:\n\n'.format(db_item['url'])
      )
      flattened_results_list = []
      for match in current_db_item['matches_data']:
            flattened_results_list.append(match)
      
      result = map(pretty_print_results, flattened_results_list)
      for val in result:
        await message.channel.send(
          '{0}'.format(val)
          )  

