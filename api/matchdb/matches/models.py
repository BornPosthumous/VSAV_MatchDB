import uuid

from urllib import parse

from django.db import models
from django.forms import ValidationError

from matchdb.constants.errors import WINNING_CHAR_ERROR, MATCHINFO_REQUIREMENT_ERROR, YOUTUBE_METADATA_ERROR

from .enums import MatchLinkType, CharNames
from django.conf import settings
# id: UUID
# type: Enum(Video/Fightcade)
# url: string
# p1_char: Enum(CharacterEnum)
# p2_char: Enum(CharacterEnum)
# created_at: string

# timestamp?: int
# title?: string
# uploader?: string
# date_uploaded?: string

# p1_name?: string
# p2_name?: string
# winning_char?: Enum(CharacterEnum)

# enum documentation: https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
# potential better way of doing enums : https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63
# ^ seems to be based on old way of handling Enums
ALLOWED_YT_NETLOCS = [
    "www.youtube.com"
]

class MatchInfo(models.Model):
    # Basic id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Is the content via Fightcade url or Video
    type = models.CharField(
        max_length=3,
        choices=MatchLinkType.choices,
    )

    # Fightcade or Video Link (usually youtube)
    url = models.URLField(max_length=200)

    # P1/P2 in game character choice
    p1_char = models.CharField(
        max_length=2,
        choices=CharNames.choices,
        default=CharNames.AN
    )
    p2_char = models.CharField(
        max_length=2,
        choices=CharNames.choices,
        default=CharNames.VI
    )
    
    winning_char = models.CharField(
        max_length=2,
        choices=CharNames.choices,
        null=True
    )

    # P1/P2 
    p1_name = models.TextField(max_length=100, default='', blank=True)
    p2_name = models.TextField(max_length=100, default='', blank=True)

    # YT info
    timestamp = models.IntegerField(default=0)
    uploader = models.TextField(max_length=100, default='')
    date_uploaded = models.DateTimeField(null=True)
    video_title = models.TextField(max_length=100, default='')

    # db internal
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    # added by
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='matches', on_delete=models.CASCADE, null=True)

    def validate_winning_char(self):
        if self.winning_char and self.winning_char not in [self.p1_char, self.p2_char]:
            raise ValidationError(WINNING_CHAR_ERROR)

    def validate_required_fields(self):
        if not self.type or not self.url:
            raise ValidationError(MATCHINFO_REQUIREMENT_ERROR)

    def validate_youtube_match(self):
        # If record is a video
        if self.type == MatchLinkType.VI:
            parsed_url = parse.urlsplit(self.url)
            # If the video is a YouTube video
            if parsed_url.netloc in ALLOWED_YT_NETLOCS:
                # It must have and uploader, date uploaded, and video title
                if not self.uploader or not self.date_uploaded or not self.video_title:
                    raise ValidationError(YOUTUBE_METADATA_ERROR)

    def save(self, *args, **kwargs):
        self.validate_required_fields()
        self.validate_youtube_match()
        self.validate_winning_char()
        super(MatchInfo, self).save(*args, **kwargs)

    def __str__(self):
        return f'<{self.__class__.__name__}> ${self.id} {self.url}'

    class Meta:
        unique_together = ['url', 'timestamp']