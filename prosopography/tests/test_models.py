import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

from prosopography.models import Person, Relationship, SocialField
from prosopography.signals.handlers import RECIPROCAL_RELATIONSHIP_MAP



FIXTURES_DIR = os.path.join(settings.BASE_DIR, 'prosopography', 'fixtures')


class TestSocialField(TestCase):

    def test_init(self):
        field = SocialField()
        assert field.db_index
        assert field.max_length == 1
        assert field.default == 'N'
        assert field.blank
        assert isinstance(field.choices, tuple)


class TestPerson(TestCase):

    def test_str_dates(self):
        quintus = Person(**{
            'nomina': 'Quintus',
            'gender': 'M',
            'cos': -25,
            'birth': 60,
            'floruit': 0,
            'death': 200,
        })

        dates = quintus.str_dates()
        print(dates['floruit'])
        assert dates['cos'] == '25 BC'
        assert dates['birth'] == 'AD 60'
        assert dates['floruit'] == '0'
        assert dates['death'] == 'AD 200'

    def test_str(self):
        # just a name
        quintus = Person(**{
            'nomina': 'Quintus',
            'gender': 'M',
        })
        assert str(quintus) == 'Quintus'

        # give a birth date
        quintus.birth = 69
        assert str(quintus) == 'Quintus (AD 69 - )'

        # give him a death date
        quintus.death = 96
        assert str(quintus) == 'Quintus (AD 69 - AD 96)'

        # give him a consulship which overrides birth/death
        quintus.cos = 90
        assert str(quintus) == 'Quintus (cos. AD 90)'

        # now just a floruit
        quintus = Person(**{
            'nomina': 'Quintus',
            'gender': 'M',
        })
        quintus.floruit = 80
        assert str(quintus) == 'Quintus (fl. AD 80)'

    def test_certainty_validator(self):
        quintus = Person.objects.create(**{
            'nomina': 'Quintus',
            'gender': 'M',
            'certainty_of_id': 5
        })
        assert quintus

        quintus.certainty_of_id = 6
        # Can save a bad value because this is form level
        quintus.save()
        # full clean, however, should choke
        with self.assertRaises(ValidationError):
            quintus.full_clean()

    def test_ordo(self):
        quintus = Person.objects.create(**{
            'nomina': 'Quintus',
            'gender': 'M',
            'certainty_of_id': 5
        })
        # consular flag
        quintus.consular = 'Y'
        assert quintus.ordo == 'Senatorial (cos.)'
        # consular and senatorial flag -- still cos.
        quintus.consular = 'Y'
        quintus.senatorial = 'Y'
        assert quintus.ordo == 'Senatorial (cos.)'
        # not consular and senatorial - senatorial
        quintus.consular = 'N'
        assert quintus.ordo == 'Senatorial'
        # equestrian and senatorial (i.e. became a senator)
        quintus.equestrian = 'Y'
        assert quintus.ordo == 'Senatorial'
        # not senatorial
        quintus.senatorial = 'M'
        assert quintus.ordo == 'Equestrian'
        # not equestrian
        quintus.equestrian = 'N'
        quintus.citizen = 'Y'
        assert quintus.ordo == 'Citizen (Not Equestrian or Senatorial)'
        # nothing
        quintus.delete()
        quintus = Person.objects.create(**{
            'nomina': 'Quintus',
            'gender': 'M',
            'certainty_of_id': 5
        })
        assert quintus.ordo == 'Non-Citizen'


class TestRelationship(TestCase):

    def setUp(self):
        self.quintus = Person.objects.create(**{
            'nomina': 'Quintus',
            'gender': 'M',
        })

        self.quinta = Person.objects.create(**{
            'nomina': 'Quinta',
            'gender': 'F',
        })

    def test_str(self):
        relationship = Relationship.objects.create(
            from_person=self.quintus,
            to_person=self.quinta,
            relationship_type='sib'
        )
        assert str(relationship) == 'Quintus - sibling to - Quinta'

    def test_signals(self):
        relationship = Relationship.objects.create(
            from_person=self.quintus,
            to_person=self.quinta,
            relationship_type='sib'
        )

        # mirror relationship created
        rev_rel = Relationship.objects.get(from_person=self.quinta)
        assert rev_rel

        # delete relationship
        relationship.delete()
        assert Relationship.objects.count() == 0

    def test_relationship_map(self):

        test_map = RECIPROCAL_RELATIONSHIP_MAP
        assert test_map['anc'] == 'des'
        assert test_map['des'] == 'anc'
        assert test_map['sib'] == 'sib'
        assert test_map['par'] == 'chi'
        assert test_map['fam'] == 'fam'
        assert test_map['ami'] == 'ami'
        assert test_map['coc'] == 'coc'
