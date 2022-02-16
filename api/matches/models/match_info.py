# from asyncio.windows_events import NULL
from django.utils import timezone
# from date import datetime 
import uuid

from django.db import models
from .. import enums

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
# winner?: boolean

# enum documentation: https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
# potential better way of doing enums : https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63
class Match_Info(models.Model):
    # Basic id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    # Is the content via Fightcade url or Video
    type = models.CharField(
        max_length=3,
        choices=enums.MatchLinkType.choices,
    )
    # Fightcade or Video Link (usually youtube)
    url = models.URLField(max_length=200)
    # P1/P2 in game character choice
    p1_char = models.CharField(
        max_length=2,
        choices=enums.CharNames.choices,
        null=True
    )
    p2_char = models.CharField(
        max_length=2,
        choices=enums.CharNames.choices,
        null=True
    )
    
    winning_char = models.CharField(
        max_length=2,
        choices=enums.CharNames.choices,
        null=True
    )
    # P1/P2 
    p1_name = models.TextField(max_length=100, default='')
    p2_name = models.TextField(max_length=100, default='')

    # YT info
    uploader = models.TextField(max_length=100, default='')
    date_uploaded = models.DateTimeField(default=timezone.now)
    timestamp = models.IntegerField(default=0)
    video_title = models.TextField(max_length=100, default='')

    # db internal
    entry_created_at = models.DateTimeField(default=timezone.now)
    entry_updated_at = models.DateTimeField(default=timezone.now)

    # added by
    added_by = models.ForeignKey('auth.User', related_name='matches', on_delete=models.CASCADE, null=True)

    # def save(self, *args, **kwargs):
    #     """
    #     Save a match~
    #     """
    #     super.save(*args, **kwargs)

    def __str__(self):
        return f'<{self.__name__}> ${self.id} {self.url}'