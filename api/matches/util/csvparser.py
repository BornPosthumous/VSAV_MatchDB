import csv
import os
import codecs
from itertools import islice
from urllib import parse
from . import alias_handler

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


def get_dict_from_csv():
    with codecs.open(os.path.join(os.path.dirname(__file__), 'match_db.csv'), 'r','UTF-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            fieldnames = reader.fieldnames 
            match_dict = []
            for row in islice(reader, 50):
                db_item = {}
                db_item['event'] = row[fieldnames[0]]
                db_item['uploader'] = row[fieldnames[1]]
                db_item['date_uploaded'] = row[fieldnames[2]]
                db_item['p1_name'] = row[fieldnames[3]]
                db_item['p2_name'] = row[fieldnames[4]]
                db_item['p1_char'] = alias_handler.get_char_enum_value_from_alias(row[fieldnames[5]])
                db_item['p2_char'] = alias_handler.get_char_enum_value_from_alias(row[fieldnames[6]])
                db_item['timestamp'] = get_stripped_url(row[fieldnames[7]])['timestamp']
                db_item['winner'] = row[fieldnames[8]]
                db_item['url'] = get_stripped_url(row[fieldnames[9]])['url']
                db_item['description'] = "None"
                db_item['video_title'] = ""
                db_item['type'] = "VI"
                match_dict.append(db_item)
            
            return match_dict
