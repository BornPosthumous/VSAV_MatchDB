from django.db import models
from django.utils.translation import gettext_lazy as _

class MatchLinkType(models.TextChoices):
    VI = 'VI', _('Video')
    FC2 = 'FC2', _('Fightcade2')

class CharNames(models.TextChoices):
    AN = 'AN', _('Anakaris')
    AU = 'AU', _('Aulbath')
    BI = 'BI', _('Bishamon')
    BU = 'BU', _('Bulleta')
    DE = 'DE', _('Demitri')
    FE = 'FE', _('Felicia')
    GA = 'GA', _('Gallon')
    JE = 'JE', _('Jedah')
    LE = 'LE', _('Lei-Lei')
    LI = 'LI', _('Lilith')
    MO = 'MO', _('Morrigan')
    SA = 'SA', _('Sasquatch')
    VI = 'VI', _('Victor')
    QB = 'QB', _('Q-Bee')
    ZA = 'ZA', _('Zabel')