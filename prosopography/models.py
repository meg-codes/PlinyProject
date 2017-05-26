from django.db import models
from django.core.exceptions import ValidationError


def valid_range(value):
    if 0 < value < 6:
        pass
    else:
        raise ValidationError('Choose a value between 1 and 5')


class SocialField(models.CharField):

    description = 'Field for modeling Roman social class identifications'

    def __init__(self, *args, **kwargs):
        DEFINITE = 'Y'
        MAYBE = 'M'
        NOT = 'N'
        UNKNOWN = 'U'
        CLASS_POSSIBILITIES = (
            (DEFINITE, 'Yes'),
            (MAYBE, 'Maybe'),
            (NOT, 'No'),
            (UNKNOWN, 'Unknown')
        )
        kwargs['max_length'] = 1
        kwargs['choices'] = CLASS_POSSIBILITIES
        kwargs['default'] = NOT
        kwargs['blank'] = True
        kwargs['db_index'] = True
        super(SocialField, self).__init__(*args, **kwargs)


class Correspondent(models.Model):
    """Persons tracked in the database to whom Pliny wrote"""

    nomina = models.CharField(max_length=255)
    # NOTE: Do I need more than this here for looonnnng nomina or should those
    # go in notes? (Probably notes)

    # Using roman convetions here
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    # default says more about Pliny's correspondents than any overarching gender
    # statement
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    # Citizenship ambiguity
    citizen = SocialField()
    equestrian = SocialField()
    senatorial = SocialField()
    consular = SocialField()

    # Certainty, expressed as 1-5, with 5 being highest and 1 being lowest
    centainty_of_id = models.PositiveSmallIntegerField(
        validators=[valid_range]
    )

    # Person notes
    notes = models.TextField()

    # related people
    related_to = models.ManyToManyField(
        'Correspondent',
        symmetrical=False,
        through='Relationship',
    )


class Relationship(models.Model):
    """A through model for a relationship between two people"""
    from_person = models.ForeignKey(Correspondent, related_name='from_person')
    to_person = models.ForeignKey(Correspondent)

    # List of controlled vocabulary and indexed relationship field
    ANCESTOR = 'anc'
    DESCENDANT = 'des'
    SIBLING = 'sib'
    PARENT = 'par'
    CHILD = 'chi'
    FAMILIA = 'fam'
    AMICUS = 'ami'
    OTHER = 'oth'

    RELATIONSHIP_TYPES = (
        (ANCESTOR, 'ancestor'),
        (DESCENDANT, 'descendant'),
        (SIBLING, 'sibling'),
        (PARENT, 'parent'),
        (CHILD, 'child'),
        (FAMILIA, 'family group'),
        (AMICUS, 'amicus'),
        (OTHER, 'otherwise related'),
    )

    relationship_type = models.CharField(
        max_length=4,
        blank=True,
        choices=RELATIONSHIP_TYPES,
        db_index=True
    )
