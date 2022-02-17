import uuid

from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from . import enums

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
class MatchInfo(models.Model):
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
        default=enums.CharNames.AN
    )
    p2_char = models.CharField(
        max_length=2,
        choices=enums.CharNames.choices,
        default=enums.CharNames.VI
    )
    
    winning_char = models.CharField(
        max_length=2,
        choices=enums.CharNames.choices,
        default=enums.CharNames.VI
    )

    # P1/P2 
    p1_name = models.TextField(max_length=100, default='')
    p2_name = models.TextField(max_length=100, default='')

    # YT info
    timestamp = models.IntegerField(default=0)
    uploader = models.TextField(max_length=100, default='')
    date_uploaded = models.DateTimeField(null=True)
    video_title = models.TextField(max_length=100, default='')

    # db internal
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    # added by
    added_by = models.ForeignKey('auth.User', related_name='matches', on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.type or not self.url:
            raise ValidationError('MatchInfo requires a type/url')
        super(MatchInfo, self).save(*args, **kwargs)
             

    # def __str__(self):
    #     return f'<{self.__name__}> ${self.id} {self.url}'