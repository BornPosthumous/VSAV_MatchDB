from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models.match_info import Match_Info
from . import enums

def save_match(request):
#    if len(Counter.objects.filter(key='counter')) == 0:
#         counter = Counter(key='counter', value=0)
#         counter.save()
#     else:
#         counter = get_object_or_404(Counter, key='counter')
    
#     counter.value+=1
#     counter.save()
#     context = {'value': counter.value}

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
