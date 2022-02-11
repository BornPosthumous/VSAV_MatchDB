import sys
sys.path.append("..") 

from database_methods import search_db_for_video, add_to_match_listing

async def remove_tag_from_video(validated):    
    if validated.get('error', None) is not None: 
      return validated

    url = validated['url']
    timestamp = validated['timestamp']
    search_results = search_db_for_video(url)

    if search_results.get('error', None) is not None: 
      return search_results

    else:
      current_db_item = search_results['result'][0]
      result = add_to_match_listing( url, timestamp, current_db_item) 
      return result 

      # flattened_results_list = []
      # for match in current_db_item['matches_data']:
      #       flattened_results_list.append(match)
      
      # result = map(pretty_print_results, flattened_results_list)
      # for val in result:
      #   await message.channel.send(
      #     '{0}'.format(val)
      #     )  

