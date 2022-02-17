from urllib import parse

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import MatchInfo, ALLOWED_YT_NETLOCS
from . import enums

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    added_by = serializers.ReadOnlyField(source='added_by.username')
    # matches = serializers.HyperlinkedIdentityField(view_name='match-list', format='html')
    id = serializers.UUIDField()

    class Meta:
        model = MatchInfo
        fields = [
            'type',
            'url',
            'p1_char',
            'p2_char',
            'winning_char',
            'p1_name',
            'p2_name',
            'timestamp'
        ]

    def validate_winning_char(self, data):
        if data['winning_char']:
            if data['winning_char'] not in [ data['p1_char'], data['p2_char'] ]:
                raise serializers.ValidationError('Winning character must be played by p1 or p2')

    def validate_required_fields(self, data):
        if not data['type'] or not data['url']:
            raise serializers.ValidationError('MatchInfo requires a type/url')

    def validate_youtube_match(self, data):
        # If record is a video
        if data['type'] == enums.MatchLinkType.VI:
            parsed_url = parse.urlsplit(data['url'])
            # If the video is a YouTube video
            if parsed_url.netloc in ALLOWED_YT_NETLOCS:
                # It must have and uploader, date uploaded, and video title
                if not data['uploader'] or not data['date_uploaded'] or not data['video_title']:
                    raise serializers.ValidationError('MatchInfo YouTube video must have metadata')

    def validate(self, data):
        self.validate_winning_char(data)
        self.validate_required_fields(data)
        self.validate_youtube_match(data)
        return data

class UserSerializer(serializers.HyperlinkedModelSerializer):
    matches = serializers.HyperlinkedRelatedField(many=True, view_name='match-detail', read_only=True)

    class Meta:
        model =  User
        fields = ['url','id','username','matches']

