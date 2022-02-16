from django.contrib.auth.models import User

from rest_framework import serializers
from .models.match_info import Match_Info

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    added_by = serializers.ReadOnlyField(source='added_by.username')
    # matches = serializers.HyperlinkedIdentityField(view_name='match-list', format='html')
    id = serializers.UUIDField()

    class Meta:
        model = Match_Info
        fields = [
            'id', 
            'type', 
            'url',
            'p1_char',
            'p2_char',
            'winner',
            'p1_name',
            'p2_name',
            'uploader',
            'date_uploaded',
            'timestamp',
            'video_title',
            'entry_created_at',
            'entry_updated_at',
            'added_by'
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    matches = serializers.HyperlinkedRelatedField(many=True, view_name='match-detail', read_only=True)

    class Meta:
        model =  User
        fields = ['url','id','username','matches']

