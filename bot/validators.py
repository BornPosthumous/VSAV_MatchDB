import re

def validate_url( url ):
  if url is None:
    return False
    
  regex = re.compile(
          r'^(?:http|ftp)s?://' # http:// or https://
          r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
          r'localhost|' #localhost...
          r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
          r'(?::\d+)?' # optional port
          r'(?:/?|[/?]\S+)$', re.IGNORECASE)
  return re.match(regex, url) is not None

def validate_match(db_item):
  missing = []
  for key in db_item:
    if db_item[key] is None:
        missing.append(key)
  
  return missing

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

all_valid = "Bulleta:\n\t{0}\nBishamon:\n\t{1}\nMorrigan:\n\t{2}\nLeiLei:\n\t{3}\nAulbath:\n\t{4}\nQ-Bee:\n\t{5}\nDemitri:\n\t{6}\nFelicia:\n\t{7}\nJedah:\n\t{8}\nAnakaris:\n\t{9}\nLilith:\n\t{10}\nSasquatch:\n\t{11}\nVictor:\n\t{12}\nZabel:\n\t{13}\nGallon:\n\t{14}".format(
    "\n\t".join(valid_bulleta),
    "\n\t".join(valid_bishamon),
    "\n\t".join(valid_morrigan),
    "\n\t".join(valid_leilei),
    "\n\t".join(valid_aulbath),
    "\n\t".join(valid_qbee),
    "\n\t".join(valid_demitri),
    "\n\t".join(valid_felicia),
    "\n\t".join(valid_jedah),
    "\n\t".join(valid_anakaris),
    "\n\t".join(valid_lilith),
    "\n\t".join(valid_sasquatch),
    "\n\t".join(valid_victor),
    "\n\t".join(valid_zabel),
    "\n\t".join(valid_gallon),
    )

def is_valid_character(char_string):
  try:
    char_string = char_string.casefold()
  except:
    return None

  if char_string in (name.casefold() for name in valid_bulleta):
      return "Bulleta"
  elif char_string in (name.casefold() for name in valid_bishamon):
      return "Bishamon"
  elif char_string in (name.casefold() for name in valid_morrigan):
      return "Morrigan"
  elif char_string in (name.casefold() for name in valid_leilei):
      return "Lei-Lei"
  elif char_string in (name.casefold() for name in valid_aulbath):
      return "Aulbath"
  elif char_string in (name.casefold() for name in valid_qbee):
      return "Q-Bee"
  elif char_string in (name.casefold() for name in valid_demitri):
      return "Demitri"
  elif char_string in (name.casefold() for name in valid_felicia):
      return "Felicia"
  elif char_string in (name.casefold() for name in valid_jedah):
      return "Jedah"
  elif char_string in (name.casefold() for name in valid_anakaris):
      return "Anakaris"
  elif char_string in (name.casefold() for name in valid_lilith):
      return "Lilith"
  elif char_string in (name.casefold() for name in valid_sasquatch):
      return "Sasquatch"
  elif char_string in (name.casefold() for name in valid_victor):
      return "Victor"
  elif char_string in (name.casefold() for name in valid_zabel):
      return "Zabel"
  elif char_string in (name.casefold() for name in valid_gallon):
      return "Gallon"
  else:
      return None