from difflib import Match
from nis import match
import uuid
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.core import serializers
from django.db.models import Q

from .models.match_info import Match_Info
from .util.csvparser import get_dict_from_csv
from . import enums
from .util import alias_handler

def seed_db_from_csv(request):
    items_to_add_dict = get_dict_from_csv()
    for tmp_match in items_to_add_dict:
        tmp_match = Match_Info(
            type             = tmp_match['type'],
            url              = tmp_match['url'],
            p1_char          = tmp_match['p1_char'],
            p2_char          = tmp_match['p2_char'],
            timestamp        = tmp_match['timestamp'],
            video_title      = tmp_match['video_title'],
            uploader         = tmp_match['uploader'],
            date_uploaded    = tmp_match['date_uploaded'],
            p1_name          = tmp_match['p1_name'],
            p2_name          = tmp_match['p2_name'],
            winner           = tmp_match['winner'],
        )
        tmp_match.save()

    return JsonResponse(items_to_add_dict, safe=False)

def delete_all_matches(self):
    Match_Info.objects.all().delete()
    return JsonResponse({'success' : True})

def get_last_n_matches(request, number_of_matches):
    # all_entries = Match_Info.objects.all().values()
    last_five_entries = list(Match_Info.objects.order_by('entry_created_at')[:number_of_matches].values())
    return JsonResponse(last_five_entries, safe=False)

def get_match_by_id(request, match_uuid):
    match = Match_Info.objects.get(id=match_uuid)
    serialized_match = serializers.serialize('json', [match])
    return JsonResponse({'match' : serialized_match}, safe=False)

def get_matchup(request, char_1 , char_2 ): 
    p1 = alias_handler.get_char_enum_value_from_alias(char_1)
    p2 = alias_handler.get_char_enum_value_from_alias(char_2)
    matchup_listing = list(
            Match_Info.objects
                .filter((Q(p1_char=p1) & Q( p2_char=p2 ) | Q(p1_char=p2) & Q( p2_char=p1 )) )
                .order_by('entry_created_at')
                .values()
        )
    return JsonResponse(matchup_listing, safe=False)

def get_matches_by_char(request, charname):
    dealiased_charname = alias_handler.get_char_enum_value_from_alias(charname)
    matches_with_charname = list(
            Match_Info.objects
                .filter(Q(p1_char=dealiased_charname) | Q(p2_char=dealiased_charname) )
                .order_by('entry_created_at')
                .values()
        )

    return JsonResponse(matches_with_charname, safe=False)

def save_test_match(request):
    match = Match_Info( 
        type             = "FC2",
        url              = "https://youtube.com",
        p1_char          = enums.CharNames.QB,
        p2_char          = enums.CharNames.SA,
        timestamp        = "420",
        video_title      = "title",
        uploader         = "feebee",
        date_uploaded    = "2021-04-20 04:20",
        p1_name          = "N-Bee",
        p2_name          = "JayOneTheSk8",
        winner           = enums.CharNames.SA,
    )
    match.save()
    return render( request, 'test.html', {
        'type'            : match.type,
        'url'             : match.url,
        'p1_char'         : match.p1_char,
        'p2_char'         : match.p2_char,
        'timestamp'       : match.timestamp,
        'video_title'     : match.video_title,
        'uploader'        : match.uploader,
        'date_uploaded'   : match.date_uploaded,
        'p1_name'         : match.p1_name,
        'p2_name'         : match.p2_name,
        'winner'          : match.winner       
    })
