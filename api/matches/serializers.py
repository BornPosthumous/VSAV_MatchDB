from rest_framework import serializers

from django.contrib.auth.models import User

from .models import MatchInfo 

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    added_by = serializers.ReadOnlyField(source='added_by.username')
    # matches = serializers.HyperlinkedIdentityField(view_name='match-list', format='html')
    id = serializers.UUIDField()

    class Meta:
        model = MatchInfo
        fields = [
            'id', 
            'type', 
            'url',
            'p1_char',
            'p2_char',
            'winning_char',
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

    def validate(self, data):
        """
            Check That winning char in p1 and p2
        """
        if data['winning_char'] is None:
            return data
        if data['winning_char'] not in [data['p1_char'],data['p2_char']]:
            raise serializers.ValidationError("winner must in p1_char or p2_char")
        return data


class UserSerializer(serializers.HyperlinkedModelSerializer):
    matches = serializers.HyperlinkedRelatedField(many=True, view_name='match-detail', read_only=True)

    class Meta:
        model =  User
        fields = ['url','id','username','matches']

