from url_parser import get_stripped_url
from validators import is_valid_character

def is_valid_timestamp(timestamp):
    try:
      timestamp = int(timestamp)
      return int(timestamp)
    except:
      return { 'error' : 'Timestamp was not a number: `{0}`\n\t\tTimestamps must be a number in seconds e.g. "100"'.format(timestamp)}
# Here are the fields we are parsing:
# Required- 
# 1. link
# 2. characters
# 3. winner/loser (to help search for games where your character won/lost
# 3. Timestamp
# optional-
# 1. player names
# 2. arcade/tournament (so bigone2nd or something like judgement day for the big 3v3 tourney)
field_validator = {
    'url':         {'fallback': None, 'transform': get_stripped_url    , 'isRequired': True  },
    'char_1':      {'fallback': None, 'transform': is_valid_character  , 'isRequired': True  },
    'char_2':      {'fallback': None, 'transform': is_valid_character  , 'isRequired': True  },
    'player_1':    {'fallback': ""  , 'transform': None                , 'isRequired': False },
    'player_2':    {'fallback': ""  , 'transform': None                , 'isRequired': False },
    'description': {'fallback': ""  , 'transform': None                , 'isRequired': False },
    'event':       {'fallback': ""  , 'transform': None                , 'isRequired': False },
    'uploader':    {'fallback': ""  , 'transform': None                , 'isRequired': False },
    'upload_date': {'fallback': ""  , 'transform': None                , 'isRequired': False },
    'winner' :     {'fallback': ""  , 'transform': is_valid_character  , 'isRequired': False },
    'timestamp' :  {'fallback': None, 'transform': is_valid_timestamp  , 'isRequired': True  },
    }


# function takes a list of fields to validate
def validate_fields( input , list_of_fields ): 
    get_timestamp_from_url = 'timestamp' not in list_of_fields
    print("get_timestamp_from_url", get_timestamp_from_url)
    result = { 
        'passed' : {},
        'failed' : []
    }
    for field in list_of_fields:
        # some inputs will just fall back to None if they are Required
        # and the supplied fallback string if they are not
        temp = input.get(field, field_validator[field]['fallback'])
        # for some values we want to transform the input as an extra validation
        if field_validator[field]['transform'] is not None:
          temp = field_validator[field]['transform'](temp)

        if field_validator[field]['isRequired'] is True and temp is None:
          result['failed'].append({ 'field': field, 'value': temp })

        elif isinstance(temp,dict) and temp['error']:
          result['failed'].append({ 'field': field, 'value': temp['error'] })

        elif isinstance(temp,dict) and field == 'url':
          result['passed']['url'] = temp['url']

          if get_timestamp_from_url is True:
            if is_valid_timestamp(temp['timestamp']):
              result['passed']['timestamp'] = temp['timestamp']
            else:
              result['failed'].append({ 'field': 'timestamp', 'value': temp['timestamp'] })
    
        else:
          result['passed'][field] = temp

    return result    

def return_validated_fields(arguments, fields_to_validate, bad_command):
    try:
      validated = validate_fields(arguments, fields_to_validate)
      failed = validated['failed']

      if len(failed):
        error_string = "The following required fields have failed to be parsed:\n"
        for failure in failed:
          error_string = error_string + "\t `{0}` : {1}\n".format(
            failure['field'],
            failure['value']
            )
        return {'error' : error_string }

    except:
      return { 'error': bad_command }

    return validated['passed']

# input = {
#     "event": "Event 2020/12/27", 
#     "uploader": "BIG-ONE2nd CHANNEL1", 
#     "date_uploaded": "Dec 26, 2020", 
#     "player_1": "", 
#     "player_2": "", 
#     "char_1": "Felicia", 
#     "char_2": "", 
#     "winner": "", 
#     "url": "https://youtu.be/Cm9UTXJZgzw?t=123", 
#     "description": "None",
#     "timestamp": "abv"
# }
# result = validate_fields(input, ['url', 'player_1','player_2', 'char_1','char_2','winner','description', 'timestamp'])
# print("result:\n" , result)