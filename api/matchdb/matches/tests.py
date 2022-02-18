import pytz
from datetime import datetime

from django.db.utils import IntegrityError
from django.test import TestCase
from django.forms import ValidationError

from matchdb.constants.errors import WINNING_CHAR_ERROR, MATCHINFO_REQUIREMENT_ERROR, YOUTUBE_METADATA_ERROR

from .models import MatchInfo
from .enums import MatchLinkType, CharNames

class TestMatchInfo(TestCase):
    def test_match_info_video(self):
        m = MatchInfo(
            type=MatchLinkType.VI,
            url='https://www.vimeo.com/vsavplaya/101011010100',
            p1_char=CharNames.BI,
            p2_char=CharNames.GA,
            winning_char=CharNames.GA,
        )
        m.save()

        db_match = MatchInfo.objects.get(id=m.id)

        self.assertEqual(db_match.type, m.type)
        self.assertEqual(db_match.url, m.url)
        self.assertEqual(db_match.p1_char, m.p1_char)
        self.assertEqual(db_match.p2_char, m.p2_char)
        self.assertEqual(db_match.winning_char, m.winning_char)

    def test_match_info_fightcade_video(self):
        m = MatchInfo(
            type=MatchLinkType.FC2,
            url='https://replay.fightcade.com/fbneo/vsav/101011010100',
            p1_char=CharNames.BI,
            p2_char=CharNames.GA,
            winning_char=CharNames.GA,
        )
        m.save()

        db_match = MatchInfo.objects.get(id=m.id)

        self.assertEqual(db_match.type, m.type)
        self.assertEqual(db_match.url, m.url)
        self.assertEqual(db_match.p1_char, m.p1_char)
        self.assertEqual(db_match.p2_char, m.p2_char)
        self.assertEqual(db_match.winning_char, m.winning_char)

    def test_match_info_youtube_video(self):
        m = MatchInfo(
            type=MatchLinkType.VI,
            url='https://www.youtube.com/Cm9UTXJZgzw',
            p1_char=CharNames.BI,
            p2_char=CharNames.GA,
            uploader = 'BIGONE',
            date_uploaded = pytz.utc.localize(datetime.now()),
            video_title = 'Bish vs Gallon',
            winning_char=CharNames.GA,
        )
        m.save()

        db_match = MatchInfo.objects.get(id=m.id)

        self.assertEqual(db_match.type, m.type)
        self.assertEqual(db_match.url, m.url)
        self.assertEqual(db_match.p1_char, m.p1_char)
        self.assertEqual(db_match.p2_char, m.p2_char)
        self.assertEqual(db_match.uploader, m.uploader)
        self.assertEqual(db_match.date_uploaded, m.date_uploaded)
        self.assertEqual(db_match.video_title, m.video_title)
        self.assertEqual(db_match.winning_char, m.winning_char)

    def test_match_info_required_fields(self):
        no_type_match = MatchInfo(
            type=MatchLinkType.FC2,
            p1_char=CharNames.BI,
            p2_char=CharNames.GA
        )
        no_url_match = MatchInfo(
            url='https://replay.fightcade.com/fbneo/vsav/101011010100',
            p1_char=CharNames.BI,
            p2_char=CharNames.GA
        )

        no_type_match_error = None
        try:
            no_type_match.save()
        except ValidationError as err:
            no_type_match_error = err.message

        no_url_match_error = None
        try:
            no_url_match.save()
        except ValidationError as err:
            no_url_match_error = err.message
        
        self.assertEqual(no_type_match_error, MATCHINFO_REQUIREMENT_ERROR)
        self.assertEqual(no_url_match_error, MATCHINFO_REQUIREMENT_ERROR)

    def test_match_info_youtube_fields(self):
        m = MatchInfo(
            type=MatchLinkType.VI,
            url='https://www.youtube.com/Cm9UTXJZgzw',
            p1_char=CharNames.BI,
            p2_char=CharNames.GA
        )

        youtube_meta_err = None
        try:
            m.save()
        except ValidationError as err:
            youtube_meta_err = err.message

        self.assertEqual(youtube_meta_err, YOUTUBE_METADATA_ERROR)

    def test_match_info_winning_char_field(self):
        m = MatchInfo(
            type=MatchLinkType.VI,
            url='https://www.vimeo.com/vsavplaya/101011010100',
            p1_char=CharNames.BI,
            p2_char=CharNames.GA,
            winning_char=CharNames.VI
        )

        winning_char_err = None
        try:
            m.save()
        except ValidationError as err:
            winning_char_err = err.message

        self.assertEqual(winning_char_err, WINNING_CHAR_ERROR)

    def test_match_info_unique_constraints(self):
        m1 = MatchInfo(
            type=MatchLinkType.VI,
            url='https://www.vimeo.com/vsavplaya/101011010100',
            p1_char=CharNames.BI,
            p2_char=CharNames.GA,
            winning_char=CharNames.GA,
            timestamp=12
        )
        m2 = MatchInfo(
            type=MatchLinkType.VI,
            url='https://www.vimeo.com/vsavplaya/101011010100',
            p1_char=CharNames.AN,
            p2_char=CharNames.MO,
            winning_char=CharNames.AN,
            timestamp=12
        )
        m1.save()

        error_thrown = False
        try:
            m2.save()
        except IntegrityError as err:
            error_thrown = True

        self.assertTrue(error_thrown)

    def test_match_info_modified_data(self):
        m = MatchInfo(
            type=MatchLinkType.VI,
            url='https://www.vimeo.com/vsavplaya/101011010100',
            p1_char=CharNames.BI,
            p2_char=CharNames.GA,
        )
        m.save()

        db_match = MatchInfo.objects.get(id=m.id)
        modified_at_time = db_match.modified_at
        created_at_time = db_match.created_at

        db_match.url = 'https://www.vimeo.com/vsavplaya/101011010111'
        db_match.save()

        updated_modified_at_time = db_match.modified_at
        updated_created_at_time = db_match.created_at

        self.assertEqual(created_at_time, updated_created_at_time)
        self.assertNotEqual(modified_at_time, updated_modified_at_time)