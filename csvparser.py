import csv
import codecs
from itertools import islice
from tinydb import TinyDB, Query
from urllib import parse

csv_path = "./match_db.csv"
db = TinyDB('./spreadsheet_db.json')
head = []
fieldnames = []

def get_stripped_url(url):
  try:
    parsed_url = parse.urlsplit(url)

    qparams = parse.parse_qs(parsed_url.query)
    fragment = parse.parse_qs(parsed_url.fragment)

    if parsed_url.netloc != "www.youtube.com" and parsed_url.netloc != "youtu.be":
      raise
    if parsed_url.netloc == "www.youtube.com":
        timestamp = None
        if qparams.get('t'):
            timestamp = qparams.get('t')[0]
        if fragment.get('t'):
            timestamp = fragment.get('t')[0]

        yt_id = qparams['v'][0].split("?")[0]

        stripped_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path + '?v=' + yt_id
        return  {'url': stripped_url, 'timestamp': timestamp}
    
    elif parsed_url.netloc == "youtu.be":
        timestamp = None
        if qparams.get('t'):
            timestamp = qparams.get('t')[0]
        if fragment.get('t'):
            timestamp = fragment.get('t')[0]

        stripped_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path
        return  {'url': stripped_url, 'timestamp': timestamp}
   
  except:
    return

current_video_urls = []
with codecs.open(csv_path, 'r', 'UTF-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        fieldnames = reader.fieldnames 
        for row in islice(reader, 50):
            db_item = {}
            db_item['event'] = row[fieldnames[0]]
            db_item['uploader'] = row[fieldnames[1]]
            db_item['date_uploaded'] = row[fieldnames[2]]
            db_item['player_1'] = row[fieldnames[3]]
            db_item['player_2'] = row[fieldnames[4]]
            db_item['char_1'] = row[fieldnames[5]]
            db_item['char_2'] = row[fieldnames[6]]
            db_item['timestamp'] = get_stripped_url(row[fieldnames[7]])['timestamp']
            db_item['winner'] = row[fieldnames[8]]
            db_item['url'] = get_stripped_url(row[fieldnames[9]])['url']
            db_item['description'] = "None"

            query_obj = Query()
            needle = db.search(query_obj.url == db_item['url'])
            if len(needle) == 0:
                db.insert({'url':db_item['url'], 'matches_data': [db_item]})
            else:
                print("noninit")
                current_db_item = needle[0]
                _current_matches = current_db_item['matches_data']
                _current_matches.append(db_item)
                current_db_item["matches_data"] = _current_matches
                db.update(current_db_item, query_obj.url == db_item['url'])
                print("added", db_item['timestamp'])
            # command_to_use = '$add_video' 
            # command = '$add_video url="{1}" player_1="{2}" char_1="{3}" player_2="{4}" char_2="{5}" winner="{6}" event="{7}" timestamp="{8}" description="{9}"'.format(
            #     command_to_use,
            #     db_item['url'],
            #     db_item['player_1'],
            #     db_item['char_1'],
            #     db_item['player_2'],
            #     db_item['char_2'],
            #     db_item['char_1'],
            #     db_item['event'],
            #     db_item['timestamp'],
            #     ""
            # )
            # match_db.insert({'url':db_item['url'], 'matches_data': [db_item]})

            # print(command)
# # print(head)
# for row in head:
#     print(row)
#     event = row[fieldnames[0]]
#     print("event", event)
#     # uploader = row[1]
#     # date_uploaded = row[2]
#     # player_1 = row[3]
#     # player_2 = row[4]
#     # char_1 = row[5]
#     # char_2 = row[6]
#     # timestamp = get_stripped_url(row[7])['timestamp']
#     # winner = row[8]
#     # url = row[9]

# print(timestamp)