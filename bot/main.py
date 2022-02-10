# Dear QA, thank you for blocking me at my day job and allowing me to complete so much work on 1/12/2021
# Native Python Libraries
import os
import sys
# python registry libraries
import discord
from tinydb import TinyDB

#local libraries
from pretty_print import pretty_print_results
from commands import (
  run_get_character_matches, 
  run_get_player_matches,
  run_get_valid_character_names, 
  run_add_video, 
  run_add_tag_to_video, 
  run_get_matchup,
  run_get_event_by_name,
  run_get_events,
  run_get_players,
  run_get_matches_from_video,
  remove_tag_from_video,
)
from help_command import get_help_command_text
# create discord client
client = discord.Client()
# we need to ping repl.it to keep the bot alive
from keep_alive import keep_alive


# Get the database instance, we re do this on every command so it is up to date
def get_db():
  db = TinyDB('./matchDB.json')
  return(db)

# this runs when the bot starts
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
      help = get_help_command_text()
      await message.channel.send( help[0] + '\n\n')
      await message.channel.send( help[1] + '\n\n')
      await message.channel.send( help[2] + '\n\n')
      await message.channel.send( help[3] )


    if message.content.startswith('$get_valid_character_names'):
      await run_get_valid_character_names(message)

    if message.content.startswith('$get_player_matches'):
      await run_get_player_matches(message, get_db())

    if message.content.startswith('$get_all_events'):
      await run_get_events(message,get_db())

    if message.content.startswith('$get_event'):
      await run_get_event_by_name(message, get_db())

    if message.content.startswith('$get_all_players'):
      await run_get_players(message, get_db())

    if message.content.startswith('$get_matches_from_video'):
      await run_get_matches_from_video(message, get_db())

    if message.content.startswith('$get_character_matches'):
      await run_get_character_matches(message, get_db())
 
    if message.content.startswith('$get_matchup'):
      await run_get_matchup(message, get_db())

    if message.content.startswith('$remove_tag_from_video'):
      await remove_tag_from_video(message, get_db())

    if message.content.startswith('$add_video'):
      await run_add_video(message, get_db())
    
    if message.content.startswith('$add_tag_to_video'):
      await run_add_tag_to_video(message, get_db())

    if message.content.startswith('$get_db'):
        match_db = get_db().all()
        flattened_results_list = []
        for sublist in match_db:
            for match in sublist['matches_data']:
                  flattened_results_list.append(match)
        result = map(pretty_print_results, flattened_results_list)
        for val in result:
          await message.channel.send(
            'Results:\n {0}'.format(val)
            )

keep_alive()

client.run(os.environ['TOKEN'])
