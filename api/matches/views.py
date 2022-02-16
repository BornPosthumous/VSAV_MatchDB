from ast import Not
from difflib import Match
from nis import match
import uuid
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.core import serializers
from django.db.models import Q

from rest_framework import generics, permissions

from django.contrib.auth.models import User

from .models.match_info import Match_Info
from .serializers import MatchSerializer, UserSerializer

from .util.csvparser import get_dict_from_csv
from . import enums
from .util import alias_handler
from rest_framework import viewsets
from rest_framework import permissions, generics
from rest_framework.decorators import action,api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions

from .serializers import UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'matches': reverse('match-list', request=request, format=format)
    })

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match_Info.objects.all()
    serializer_class = MatchSerializer
    lookup_url_kwarg = "uuid"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Add entry uploader on creation of match info 
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

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
            raise ValidationError("p1_char and p2_char must be provided")
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
        query_params = request.query_params
        char = query_params.get('char', None)
        if char is None:
            raise ValidationError("char must be provided")
        # check aliases
        dealiased_charname = alias_handler.get_char_enum_value_from_alias(char)
        queryset = list(
                Match_Info.objects
                    .filter(Q(p1_char=dealiased_charname) | Q(p2_char=dealiased_charname) )
                    .order_by('entry_created_at')
                    .values()
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


# TODO: Will this work for fc2 or throw error?
def get_matches_from_video(request):
    url = request.GET.getlist('url')[0]
    matches_by_url = list(
        Match_Info.objects.filter(Q(url=url))
        .order_by('timestamp')
        .values()
    )
    return JsonResponse(matches_by_url, safe=False)



##########################################################
# Various ways of structuring rest framework auto APIs for Matches
##########################################################
# class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Match_Info.objects.all()
#     serializer_class = MatchSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
# class MatchList(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = Match_Info.objects.all()
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
#         snippets = Match_Info.objects.all()
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
#             match = Match_Info.objects.get(id=match_uuid)
#         except Match_Info.DoesNotExist:
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#     def get(self, request, match_uuid, format=None):
#         match = self.get_object(match_uuid)
#         serializer = MatchSerializer(match)
#         return Response(serializer.data)

#     def put(self, request, match_uuid, format=None):
#         match = self.get_object(match_uuid)
#         serializer = Match_Info(match, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request, match_uuid, format=None):
#         match = self.get_object(match_uuid)
#         match.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


