import os

from django.forms import ValidationError
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q

from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action,api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions

from .models import MatchInfo
from .serializers import MatchSerializer

from .util.csvparser import get_dict_from_csv
from . import enums
from .util import alias_handler, youtube

@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root Documentation. Please see the major routes below:

    ### __Matches__: [/matches/](/vsav_info/matches/)
    """
    return Response({
        'matches': reverse('matches-list', request=request, format=format)
    })

class MatchViewSet(viewsets.ModelViewSet):
    """
    Match Info Documentation 

    Many Query Parameters require a valid character alias. Here is a list of valid aliases:

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

    ### matches/by_character:
    Search for matches that include the given character.

    Query Params:

    - __char__  : string = valid character alias.

    Example : [matches/by-character?char=MO](/vsav_info/matches/by-character?char=MO)
    
    ### get-latest
    Get last n matches

    Search for matches that include the given character.

    Query Params:

    - number_of_matches__  : int = number to return

    Example : [matches/get-latest?number_of_matches=5](/vsav_info/matches/get-latest?number_of_matches=5)

    ### matches/get-matchup:
    Search for matches that include the given character.

    Query Params:

    - __char1__: Character Short Name or Alias
    - __char2__: Character Short Name or Alias
   
    Example : [matches/get-matchup/?char1=GA&char2=FE](/vsav_info/matches/get-matchup/?char1=GA&char2=FE)
    
    """
    queryset = MatchInfo.objects.all()
    serializer_class = MatchSerializer
    # Right now we are using uuid, and not DRFs default of primary key (pk:int)
    # This sets up how the route for detail should be accessed
    lookup_url_kwarg = "uuid"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        video_url = request.data.get('url')
        serializer = self.get_serializer(data=request.data)
        if youtube.is_youtube_url(video_url):
            video_details = youtube.request_video_details(video_url)
            # pass this into the match model
            request.data['uploader'] = video_details['uploader']
            request.data['date_uploaded'] = video_details['date_uploaded']
            request.data['video_title'] = video_details['video_title']

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Add entry uploader on creation of match info item 
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    @action(methods=['get'], detail=False, url_path='get-yt-info', url_name='get_yt_info' )
    def get_yt_info(self, request):
        video_url = request.data.get('url')
        if youtube.is_youtube_url(video_url):
            video_details = youtube.request_video_details(video_url)
            # pass this into the match model
            resp = {
                'uploader' : video_details.uploader,
                'date_uploaded': video_details.date_uploaded,
                'video_title' : video_details.video_title,
            }
            return Response(resp, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_path='get-latest', url_name='get_latest' )
    def get_latest(self, request):
        """
            Get the last n matches
            Required Query Parameter:
                ?number_of_matches: Int 
        """
        query_params = request.query_params
        num_to_get = query_params.get('number_of_matches', None)

        if num_to_get is not None:
            try:
                num_to_get = int(num_to_get)
                queryset = self.queryset.order_by('entry_created_at')[:num_to_get].values()
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            except:
                raise ValidationError("Number_of_matches must be an integer")
        else:
            raise ValidationError("Number_of_matches must be an integer")

    @action(methods=['get'], detail=False, url_path='get-matchup', url_name='get_matchup' )
    def get_matchup(self, request):
        """
            Get a listing of char1 vs char2
            Required Query Parameters:
                char1: Character Short Name or Alias
                char2: Character Short Name or Alias
        """

        query_params = request.query_params
        char1 = query_params.get('char1', None)
        char2 = query_params.get('char2', None)
        if char1 is None or char2 is None:
            raise ValidationError("char1 and char2 must be provided")
        # check aliases
        p1 = alias_handler.get_char_enum_value_from_alias(char1)
        p2 = alias_handler.get_char_enum_value_from_alias(char2)
        queryset = list(
            self.queryset
                .filter((Q(p1_char=p1) & Q( p2_char=p2 ) | Q(p1_char=p2) & Q( p2_char=p1 )) )
                .order_by('entry_created_at')
                .values()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='by-character', url_name='by_character' )
    def by_character(self, request):
        """
            Will list all of the urls that have been tagged with the character specified in the char query param.
        """
        query_params = request.query_params
        char = query_params.get('char', None)
        if char is None:
            raise ValidationError("char must be provided")
        # check aliases
        dealiased_charname = alias_handler.get_char_enum_value_from_alias(char)
        queryset = list(
                MatchInfo.objects
                    .filter(Q(p1_char=dealiased_charname) | Q(p2_char=dealiased_charname) )
                    .order_by('entry_created_at')
                    .values()
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='by-url', url_name='by_url' )
    def by_url(self, request):
        """
            Get all timestamps from a video
            Required Query Parameters:
            ?url: A timestampable video
        """
        query_params = request.query_params
        url = query_params.get('url', None)
        
        if url is None:
            raise ValidationError("url must be provided")
        
        queryset = list(
            MatchInfo.objects.filter(Q(url=url) & Q(type=enums.MatchLinkType.VI))
            .order_by('timestamp')
            .values()
        ) 

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

def seed_test_data_from_csv(request):
    items_to_add_dict = get_dict_from_csv()
    for tmp_match in items_to_add_dict:
        tmp_match = MatchInfo(
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
            winning_char     = tmp_match['winner'],
        )
        tmp_match.save()

    return JsonResponse(items_to_add_dict, safe=False)

def delete_all_matches(self):
    MatchInfo.objects.all().delete()
    return JsonResponse({'success' : True})

##########################################################
# Various ways of structuring rest framework auto APIs for Matches
##########################################################
# class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MatchInfo.objects.all()
#     serializer_class = MatchSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
# class MatchList(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = MatchInfo.objects.all()
#     serializer_class = MatchSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class MatchList(APIView):
#     """
#     List all matches, or create a new match.
#     """
#     def get(self, request, format=None):
#         snippets = MatchInfo.objects.all()
#         serializer = MatchSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = MatchSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MatchDetail(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView,
# ):
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class MatchDetail(APIView):
#     """
#     Retrieve, update or delete a matches info.
#     """
#     def get_object(self, match_uuid):
#         try:
#             match = MatchInfo.objects.get(id=match_uuid)
#         except MatchInfo.DoesNotExist:
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#     def get(self, request, match_uuid, format=None):
#         match = self.get_object(match_uuid)
#         serializer = MatchSerializer(match)
#         return Response(serializer.data)

#     def put(self, request, match_uuid, format=None):
#         match = self.get_object(match_uuid)
#         serializer = MatchInfo(match, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request, match_uuid, format=None):
#         match = self.get_object(match_uuid)
#         match.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


