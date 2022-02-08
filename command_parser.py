import shlex 
from urllib import parse
from validators import is_valid_character


def parse_get_matches_from_video(message, command):
  message = message.replace(command, '')
  split_message = shlex.split(message)
  url = split_message[0]
  try:
    parsed_url = get_stripped_url(url)
    split_url = parsed_url['url']
  except:
      return "An invalid url was supplied or was missing"

  return split_url


def parse_matchup_command(message, command):
  #get rid of command
  message = message.replace(command, '')
  split_message = shlex.split(message)
  char_1 = is_valid_character(split_message[0])
  char_2 = is_valid_character(split_message[2])
  return { 'char_1': char_1, 'char_2': char_2}

def parse_get_event(message, command):
  #get rid of command
  message = message.replace(command, '')
  split_message = shlex.split(message)
  event = split_message[0]
  return event

class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


# Here are the fields we are parsing:
# Required- 
# 1. link
# 2. characters
# 3. winner/loser (to help search for games where your character won/lost
# 3. Timestamp
# optional-
# 1. player names
# 2. arcade/tournament (so bigone2nd or something like judgement day for the big 3v3 tourney)
def parse_db_item(parsed):
  db_item = {}

  db_item['url'] = parsed.get('url', None)

  player_1 = parsed.get("player_1", "")
  db_item['player_1'] = player_1 

  player_2 = parsed.get("player_2", "")
  db_item['player_2'] = player_2

  char_1 = parsed.get("char_1", None)
  db_item['char_1'] = is_valid_character(char_1)

  char_2 = parsed.get("char_2", None)
  db_item['char_2'] = is_valid_character(char_2)

  winner = parsed.get("winner", None)
  db_item['winner'] = is_valid_character(winner)

  event = parsed.get("event", "Casuals")
  db_item['event'] = event

  description = parsed.get("description", "")
  db_item['description'] = description

  timestamp = parsed.get("timestamp", None)

  try:
    timestamp = int(timestamp)
  except:
    timestamp = None

  db_item['timestamp'] = timestamp
 
  # db_item['matches'] = []

  return db_item
# example twitch url:
# https://www.twitch.tv/videos/863002509?t=00h10m42s
def get_stripped_url(url):
  try:
    parsed_url = parse.urlsplit(url)

    qparams = parse.parse_qs(parsed_url.query)
    fragment = parse.parse_qs(parsed_url.fragment)
    if parsed_url.netloc != "www.youtube.com":
      raise

    timestamp = None
    if qparams.get('t'):
        timestamp = qparams.get('t')[0]
    if fragment.get('t'):
        timestamp = fragment.get('t')[0]

    yt_id = qparams['v'][0].split("?")[0]

    stripped_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path + '?v=' + yt_id
    return  {'url': stripped_url, 'timestamp': timestamp}
  except:
    raise

def parse_command(message, command):
  # # Remove the command itself
  message = message.replace(command, '')
  # $test_argument_splitter one=1 two=2 three=3
  split_message = shlex.split(message)

  # Split into a dictionary
  # [ 'one=1', 'two=2', 'three=3' ]
  split_args = dict(item.split('=',1) for item in split_message)
  # # Result: {'one': '1', 'two': '2', 'three': '3'}
  if split_args.get("url", None):
    try:
      url = split_args.get("url", None)
      parsed_url = get_stripped_url(url)
      split_args['url'] = parsed_url['url']
      if parsed_url['timestamp'] is not None:
        split_args['timestamp'] = parsed_url['timestamp']
    except:
      return ""

  return split_args
  