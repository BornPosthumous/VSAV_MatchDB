import csv
import os
import codecs
from itertools import islice
from urllib import parse
from ..enums import CharNames

csv_path = "api/matches/util/match_db.csv"

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


valid_bulleta   = ["Bulleta", "B.B. Hood", "BU", "BB Hood", "BBHood"]
valid_bishamon  = ["Bishamon", "BI"]
valid_morrigan  = ["Morrigan", "MO"]
valid_leilei    = ["Lei-Lei", "LeiLei", "Hsien-Ko", "HsienKo", "Lei Lei"]
valid_aulbath   = ["Aulbath", "Fish", "AU", "Rikuo"]
valid_qbee      = ["QB", "Q-Bee", "Bee", "QBee", "Q Bee"]
valid_demitri   = ["Demitri", "DE"]
valid_felicia   = ["FE", "Felicia", "Cat"]
valid_jedah     = ["JE", "Jedah"]
valid_anakaris  = ["Anakaris", "AN"]
valid_lilith    = ["Lilith", "LI"]
valid_sasquatch = ["Sasquatch", "SA","SAS"]
valid_victor    = ["Victor", "VI"]
valid_zabel     = ["Zabel", "ZA", "Raptor", "Zombie"]
valid_gallon    = ["Gallon", "GA", "Talbain", "Wolf", "J Talbain", "JTalbain"]
def get_char_enum_value_from_alias(char_string):
    try:
        char_string = char_string.casefold()
    except:
        return None

    if char_string in (name.casefold() for name in valid_bulleta):
        return CharNames.BU
    elif char_string in (name.casefold() for name in valid_bishamon):
        return CharNames.BI
    elif char_string in (name.casefold() for name in valid_morrigan):
        return CharNames.MO
    elif char_string in (name.casefold() for name in valid_leilei):
        return CharNames.LE
    elif char_string in (name.casefold() for name in valid_aulbath):
        return CharNames.AU
    elif char_string in (name.casefold() for name in valid_qbee):
        return CharNames.QB
    elif char_string in (name.casefold() for name in valid_demitri):
        return CharNames.DE
    elif char_string in (name.casefold() for name in valid_felicia):
        return CharNames.FE
    elif char_string in (name.casefold() for name in valid_jedah):
        return CharNames.JE
    elif char_string in (name.casefold() for name in valid_anakaris):
        return CharNames.AN
    elif char_string in (name.casefold() for name in valid_lilith):
        return CharNames.LI
    elif char_string in (name.casefold() for name in valid_sasquatch):
        return CharNames.SA
    elif char_string in (name.casefold() for name in valid_victor):
        return CharNames.VI
    elif char_string in (name.casefold() for name in valid_zabel):
        return CharNames.ZA
    elif char_string in (name.casefold() for name in valid_gallon):
        return CharNames.GA
    else:
        return None

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
                db_item['p1_char'] = get_char_enum_value_from_alias(row[fieldnames[5]])
                db_item['p2_char'] = get_char_enum_value_from_alias(row[fieldnames[6]])
                db_item['timestamp'] = get_stripped_url(row[fieldnames[7]])['timestamp']
                db_item['winner'] = row[fieldnames[8]]
                db_item['url'] = get_stripped_url(row[fieldnames[9]])['url']
                db_item['description'] = "None"
                db_item['video_title'] = ""
                db_item['type'] = "VI"
                match_dict.append(db_item)
            
            return match_dict

            # query_obj = Query()
            # needle = db.search(query_obj.url == db_item['url'])
            # if len(needle) == 0:
            #     db.insert({'url':db_item['url'], 'matches_data': [db_item]})
            # else:
            #     print("noninit")
            #     current_db_item = needle[0]
            #     _current_matches = current_db_item['matches_data']
            #     _current_matches.append(db_item)
            #     current_db_item["matches_data"] = _current_matches
            #     db.update(current_db_item, query_obj.url == db_item['url'])
            #     print("added", db_item['timestamp'])
