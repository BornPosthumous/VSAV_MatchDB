from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict

from .models.match_info import Match_Info
from .util.csvparser import get_dict_from_csv
from . import enums

from django.core import serializers

def seed_db_from_csv(request):
    items_to_add_dict = get_dict_from_csv()
    for tmp_match in items_to_add_dict:
        print(tmp_match)
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
    print(items_to_add_dict)
    return JsonResponse(items_to_add_dict, safe=False)

def get_last_five_matches(request):
    # all_entries = Match_Info.objects.all().values()
    last_five_entries = list(Match_Info.objects.order_by('entry_created_at')[:5].values())
    return JsonResponse(last_five_entries, safe=False)

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
        winner           = enums.CharNames.AN,
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
