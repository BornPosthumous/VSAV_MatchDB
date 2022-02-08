def pretty_print_results(db_item):
  return "{0} ( {1} ) vs {2} ( {3} ) at {4} \n\t <{5}> \n\t`{6}`\n".format(
      db_item['player_1'],
      db_item['char_1'],
      db_item['player_2'],
      db_item['char_2'],
      db_item['event'],
      (db_item['url']+'?t='+str(db_item['timestamp']) ), #  https://youtu.be/tsH0ffvfjXM?t=32
      db_item['description']
  )  

