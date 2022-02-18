from ..enums import CharNames

valid_bulleta   = {'enum_value_from_db' : CharNames.BU , 'aliases' : ["Bulleta", "B.B. Hood", "BU", "BB Hood", "BBHood"]}
valid_bishamon  = {'enum_value_from_db' : CharNames.BI , 'aliases' : ["Bishamon", "BI"]}
valid_morrigan  = {'enum_value_from_db' : CharNames.MO , 'aliases' : ["Morrigan", "MO"]}
valid_leilei    = {'enum_value_from_db' : CharNames.LE , 'aliases' : ["Lei-Lei", "LeiLei", "Hsien-Ko", "HsienKo", "Lei Lei"]}
valid_aulbath   = {'enum_value_from_db' : CharNames.AU , 'aliases' : ["Aulbath", "Fish", "AU", "Rikuo"]}
valid_qbee      = {'enum_value_from_db' : CharNames.QB , 'aliases' : ["QB", "Q-Bee", "Bee", "QBee", "Q Bee", "Q. Bee"]}
valid_demitri   = {'enum_value_from_db' : CharNames.DE , 'aliases' : ["Demitri", "DE"]}
valid_felicia   = {'enum_value_from_db' : CharNames.FE , 'aliases' : ["FE", "Felicia", "Cat"]}
valid_jedah     = {'enum_value_from_db' : CharNames.JE , 'aliases' : ["JE", "Jedah"]}
valid_anakaris  = {'enum_value_from_db' : CharNames.AN , 'aliases' : ["Anakaris", "AN"]}
valid_lilith    = {'enum_value_from_db' : CharNames.LI , 'aliases' : ["Lilith", "LI"]}
valid_sasquatch = {'enum_value_from_db' : CharNames.SA , 'aliases' : ["Sasquatch", "SA","SAS"]}
valid_victor    = {'enum_value_from_db' : CharNames.VI , 'aliases' : ["Victor", "VI"]}
valid_zabel     = {'enum_value_from_db' : CharNames.ZA , 'aliases' : ["Zabel", "ZA", "Raptor", "Zombie"]}
valid_gallon    = {'enum_value_from_db' : CharNames.GA , 'aliases' : ["Gallon", "GA", "Talbain", "Wolf", "J Talbain", "JTalbain", 'J. Talbain']}

def get_char_enum_value_from_alias(char_string):
    try:
        char_string = char_string.casefold()
    except:
        return None
    print("Trying...",char_string)
    if char_string in (name.casefold() for name in valid_bulleta['aliases']):
        return CharNames.BU
    elif char_string in (name.casefold() for name in valid_bishamon['aliases']):
        return CharNames.BI
    elif char_string in (name.casefold() for name in valid_morrigan['aliases']):
        return CharNames.MO
    elif char_string in (name.casefold() for name in valid_leilei['aliases']):
        return CharNames.LE
    elif char_string in (name.casefold() for name in valid_aulbath['aliases']):
        return CharNames.AU
    elif char_string in (name.casefold() for name in valid_qbee['aliases']):
        return CharNames.QB
    elif char_string in (name.casefold() for name in valid_demitri['aliases']):
        return CharNames.DE
    elif char_string in (name.casefold() for name in valid_felicia['aliases']):
        return CharNames.FE
    elif char_string in (name.casefold() for name in valid_jedah['aliases']):
        return CharNames.JE
    elif char_string in (name.casefold() for name in valid_anakaris['aliases']):
        return CharNames.AN
    elif char_string in (name.casefold() for name in valid_lilith['aliases']):
        return CharNames.LI
    elif char_string in (name.casefold() for name in valid_sasquatch['aliases']):
        return CharNames.SA
    elif char_string in (name.casefold() for name in valid_victor['aliases']):
        return CharNames.VI
    elif char_string in (name.casefold() for name in valid_zabel['aliases']):
        return CharNames.ZA
    elif char_string in (name.casefold() for name in valid_gallon['aliases']):
        return CharNames.GA
    else:
        return None