from django.db import models
from django.core.exceptions import ValidationError


def valid_range(value):
    if 0 < value < 6:
        pass
    else:
        raise ValidationError('Choose a value between 1 and 5')


class SocialField(models.CharField):
    """Subclass of :class:`django.db.models.CharField` that adds restrictions
    on field choices and defaults for recording social class certainty.
    """
    description = 'Field for modeling Roman social class identifications'

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

    def __init__(self, *args, **kwargs):

        kwargs['max_length'] = 1
        kwargs['choices'] = self.CLASS_POSSIBILITIES
        kwargs['default'] = self.NOT
        kwargs['blank'] = True
        kwargs['db_index'] = True
        super(SocialField, self).__init__(*args, **kwargs)


class AKA(models.Model):
    """Alternate names for individuals to account for common searches or
    confusions"""
    nomina = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    person = models.ForeignKey('Person')


class Person(models.Model):
    """Persons tracked in the database to whom Pliny wrote or mentioned in his
    letters.

    """

    nomina = models.CharField(max_length=255)
    # NOTE: Do I need more than this here for looonnnng nomina or should those
    # go in notes? (Probably notes)

    # Using roman convetions here
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    # default says more about Pliny's correspondents than any overarching
    # statement about gender.
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    # Citizenship ambiguity
    citizen = SocialField()
    equestrian = SocialField()
    senatorial = SocialField()
    consular = SocialField()

    # years, all optional
    birth = models.NullBooleanField(blank=True, null=True)
    death = models.NullBooleanField(blank=True, null=True)
    cos = models.NullBooleanField(blank=True, null=True)
    floruit = models.NullBooleanField(blank=True, null=True)

    # Certainty, expressed as 1-5, with 5 being highest and 1 being lowest
    # Low uncertainty expresses overall issues with identification
    certainty_of_id = models.PositiveSmallIntegerField(
        validators=[valid_range],
        default=5,
    )

    # Letter Foreign Keys
    letters_to = models.ManyToManyField(
        'letters.Letter',
        related_name='letters_to',
        blank=True,
        verbose_name='letter to'
    )
    mentioned_in = models.ManyToManyField(
        'letters.Letter',
        related_name='mentioned_in',
        blank=True
    )

    # Person notes
    notes = models.TextField(blank=True)

    # related people
    related_to = models.ManyToManyField(
        'Person',
        symmetrical=False,
        through='Relationship',
    )

    def str_dates(self):
        '''Produce BC/AD strings of any integer dates'''
        date_fields = ['birth', 'death', 'cos', 'floruit']
        dates = {}
        for field in date_fields:
            value = getattr(self, field)
            if value and value < 0:
                value = ('%s BC' % value).replace('-', '')
            elif value and value > 0:
                value = 'AD %s' % value
            dates[field] = str(value)

        return dates

    def __str__(self):
        dates = self.str_dates()
        if self.cos:
            return '%s (cos. %s)' % (self.nomina, dates['cos'])
        if self.birth or self.death:
            return (
                '%s (%s - %s)' %
                (self.nomina, dates['birth'], dates['death'])
            ).replace('null', '').replace('None', '')
        if self.floruit:
            return '%s (fl. %s)' % (self.nomina, dates['floruit'])
        return self.nomina

    @property
    def ordo(self):
        """The returns the social class of the :class:`Person` as a simple string based
        on the social class flags set."""
        if self.consular == 'Y':
            return 'Senatorial (cos.)'
        if self.senatorial == 'Y':
            return 'Senatorial'
        if self.equestrian == 'Y' :
            return 'Equestrian'
        if self.citizen == 'Y':
            return 'Citizen (Not Equestrian or Senatorial)'

        return 'Non-Citizen'

class Relationship(models.Model):
    """A through model for a relationship between two people"""
    from_person = models.ForeignKey(Person, related_name='from_person')
    to_person = models.ForeignKey(Person)

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
        (FAMILIA, 'member of same familia'),
        (AMICUS, 'amicus'),
        (OTHER, 'otherwise related'),
    )

    relationship_type = models.CharField(
        max_length=4,
        choices=RELATIONSHIP_TYPES,
        db_index=True
    )

    def __str__(self):
        return '%s - %s to - %s' % (
            self.from_person,
            self.get_relationship_type_display(),
            self.to_person
        )
