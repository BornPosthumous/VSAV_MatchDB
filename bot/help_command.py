
help_sample = "$help"
help_description = "help_description"

get_valid_character_names_sample = "$get_valid_character_names" 
get_valid_character_names_description = "Returns a list of allowed aliases for characters."

get_player_matches_sample = '$get_player_matches "BUZZ"' 
get_player_matches_description = "Returns matches in the database that this player is tagged in. This is not a required field"

get_all_events_sample = "$get_all_events" 
get_all_events_description = 'Returns a list of event names in the database. You may get all of the matches in an event with the $get_event command '

get_event_sample = '$get_event "Mikado Showdown"'
get_event_description = "Returns a list of matches in an event. You may get a list of events with the $get_all_events command"

get_all_players_sample = "$get_all_players" 
get_all_players_description = "Returns a list of all players in the database. You may get a list of matches played by a player with the $get_player_matches command"

get_matches_from_video_sample = "$get_matches_from_video  https://www.youtube.com/watch?v=tsH0ffvfjXM?t=30" 
get_matches_from_video_description = "Returns a list of matches tagged within the specified youtube video"

get_character_matches_sample = '$get_character_matches "Sasquatch"'
get_character_matches_description = "Returns a list of matches containing the specified character. You may get a listing of character aliases with the $get_valid_character_names command"

get_matchup_sample = '$get_matchup "Sasquatch" vs "Gallon"' 
get_matchup_description = "Returns a list of videos containing the specified characters."

remove_tag_from_video_sample = '$remove_tag_from_video url="https://www.youtube.com/watch?v=tsH0ffvfjXM?t=30" timestamp="90"' 
remove_tag_from_video_description = "Remove a tag from the video. This is used for editing purposes. The timestamp must be specified in seconds."

add_video_sample = '$add_video url="https://www.youtube.com/watch?v=tsH0ffvfjXM&feature=youtu.be" player_1="BUZZ" char_1="Gallon" player_2="DD" char_2="Sasquatch" winner="wolf" event="Mikado Showdown" timestamp="30" description="hello hello thats some AWOOOOOO"' 
add_video_description = "Add a video to the database. Videos must be from youtube. The character , winner, and timestamp fields are required. Timestamps must be in seconds"

add_tag_to_video_sample = '$add_tag_to_video url="https://www.youtube.com/watch?v=tsH0ffvfjXM" player_1="Test1" char_1="qbee" player_2="Test2" char_2="anakaris" winner="qbee" timestamp="90" event="Mikado Showdown" description="Second test description"' 
add_tag_to_video_description = "Tags a match for the specified video. The character , winner, and timestamp fields are required. Timestamps must be in seconds. The video must not already exist in the database."

def get_help_command_text():
    help_data_1 = [
      { 'command': '$help', 
        'sample': help_sample,
        'description': help_description,
      },
      { 'command': '$get_valid_character_names', 
        'sample': get_valid_character_names_sample,
        'description': get_valid_character_names_description,
      },
      {
        'command':'$get_player_matches',
        'sample': get_player_matches_sample,
        'description': get_player_matches_description
      },
      {
        'command': '$get_all_events',
        'sample': get_all_events_sample,
        'description': get_all_events_description
      }]
    help_data_2 = [{
        'command': '$get_event',
        'sample': get_event_sample,
        'description': get_event_description
      },
      {
        'command': '$get_all_players',
        'sample': get_all_players_sample,
        'description': get_all_players_description
      },
      {
        'command': '$get_matches_from_video',
        'sample': get_matches_from_video_sample,
        'description': get_matches_from_video_description
      },
      {
        'command': '$get_event',
        'sample': get_event_sample,
        'description': get_event_description
      },
      {
        'command': '$get_all_players',
        'sample': get_all_players_sample,
        'description': get_all_players_description
      },
    ]
    help_data_3 = [
      {
        'command': '$get_matches_from_video',
        'sample': get_matches_from_video_sample,
        'description': get_matches_from_video_description
      },
      {
        'command': '$get_character_matches',
        'sample': get_character_matches_sample,
        'description': get_character_matches_description
      },
      {
        'command': '$get_matchup',
        'sample': get_matchup_sample,
        'description': get_matchup_description
      },
    ]
    help_data_4 = [ 
      {
        'command': '$remove_tag_from_video',
        'sample': remove_tag_from_video_sample,
        'description': remove_tag_from_video_description
      },
      {
        'command': '$add_video',
        'sample': add_video_sample,
        'description': add_video_description
      },
      {
        'command': '$add_tag_to_video',
        'sample': add_tag_to_video_sample,
        'description': add_tag_to_video_description
      },
    ]
    parsed_help_data_1 = []
    parsed_help_data_2 = []
    parsed_help_data_3 = []
    parsed_help_data_4 = []
    for help_item in help_data_1:
      parsed = "`{0}`\n\tSample Usage: `{1}`\n\tDescription: `{2}`\n\n".format( 
        help_item['command'],
        help_item['sample'],
        help_item['description'],
        )
      parsed_help_data_1.append(parsed)

    for help_item in help_data_2:
      parsed = "`{0}`\n\tSample Usage: `{1}`\n\tDescription: `{2}`\n\n".format( 
        help_item['command'],
        help_item['sample'],
        help_item['description'],
        )
      parsed_help_data_2.append(parsed)
    for help_item in help_data_3:
      parsed = "`{0}`\n\tSample Usage: `{1}`\n\tDescription: `{2}`\n\n".format( 
        help_item['command'],
        help_item['sample'],
        help_item['description'],
        )
      parsed_help_data_3.append(parsed)

    for help_item in help_data_4:
      parsed = "`{0}`\n\tSample Usage: `{1}`\n\tDescription: `{2}`\n\n".format( 
        help_item['command'],
        help_item['sample'],
        help_item['description'],
        )
      parsed_help_data_4.append(parsed)
    joined_1 = "".join(parsed_help_data_1)
    joined_2 = "".join(parsed_help_data_2)
    joined_3 = "".join(parsed_help_data_3)
    joined_4 = "".join(parsed_help_data_4)
    return [joined_1, joined_2, joined_3, joined_4]
