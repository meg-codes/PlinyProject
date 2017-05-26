from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Correspondent, SocialField


class TestSocialField(TestCase):

    def test_init(self):
        field = SocialField()
        assert field.db_index
        assert field.max_length == 1
        assert field.default == 'N'
        assert field.blank
        assert isinstance(field.choices, tuple)

class TestCorrespondent(TestCase):

    def test_str_dates(self):
        quintus = Correspondent(**{
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
        quintus = Correspondent(**{
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
        quintus = Correspondent(**{
            'nomina': 'Quintus',
            'gender': 'M',
        })
        quintus.floruit = 80
        assert str(quintus) == 'Quintus (fl. AD 80)'

    def test_certainty_validator(self):
        quintus = Correspondent.objects.create(**{
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
