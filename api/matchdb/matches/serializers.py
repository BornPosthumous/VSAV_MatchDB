import re

from multiprocessing.spawn import import_main_path
from urllib.parse import urlparse, parse_qs
from urllib import parse

from rest_framework import serializers

from matchdb.constants.errors import WINNING_CHAR_ERROR, MATCHINFO_REQUIREMENT_ERROR, YOUTUBE_METADATA_ERROR

from .models import MatchInfo, ALLOWED_YT_NETLOCS
from .enums import MatchLinkType

class MatchSerializer(serializers.HyperlinkedModelSerializer):

    added_by = serializers.ReadOnlyField(source='added_by.username', read_only=True)
    id = serializers.UUIDField(read_only=True)

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
            'timestamp',
            'added_by',
            'date_uploaded',
            'video_title',
            'uploader'
        ]

    def validate_winning_character(self, data):
        if data['winning_char'] is not None and data['winning_char']:
            if data['winning_char'] not in [ data['p1_char'], data['p2_char'] ]:
                raise serializers.ValidationError(WINNING_CHAR_ERROR)

    def validate_required_fields(self, data):
        if not data['type'] or not data['url']:
            raise serializers.ValidationError(MATCHINFO_REQUIREMENT_ERROR)

    def validate_youtube_match(self, data):
        # If record is a video
        if data['type'] == MatchLinkType.VI:
            parsed_url = parse.urlsplit(data['url'])
            # If the video is a YouTube video
            if parsed_url.netloc in ALLOWED_YT_NETLOCS:
                # It must have and uploader, date uploaded, and video title
                missing_uploader = 'uploader' in data and data['uploader'] is None
                missing_date_uploaded = 'date_uploaded' in data and data['date_uploaded'] is None
                missing_video_title = 'video_title' in data and data['video_title'] is None
                if data and (missing_date_uploaded or missing_uploader or missing_video_title) :
                    raise serializers.ValidationError(YOUTUBE_METADATA_ERROR)

    def validate(self, data):
        self.validate_winning_character(data)
        self.validate_required_fields(data)
        self.validate_youtube_match(data)
        return data

    def get_youtube_video_id(yt_url):
        parsed_url = urlparse(yt_url)
        return parse_qs(parsed_url.query)['v'][0]

    def is_youtube_url(url):
        youtube_regex = r'(https?:\/\/)?((www\.)?(youtube(-nocookie)?|youtube.googleapis)\.com.*(v\/|v=|vi=|vi\/|e\/|embed\/|user\/.*\/u\/\d+\/)|youtu\.be\/)([_0-9a-z-]+)'
        youtube_regex_match = re.match(youtube_regex, url)
        return bool(youtube_regex_match)
