import os
import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import AKA, Person, Relationship, SocialField
from letters.models import Letter
from prosopography.management.commands import import_pliny_data

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
        print(relationship)
        assert str(relationship) == 'Quintus - sibling to - Quinta'

class TestImport(TestCase):

    def setUp(self):
        self.letters = os.path.join(FIXTURES_DIR, 'letters.csv')
        self.people = os.path.join(FIXTURES_DIR, 'people.csv')
        self.importer = import_pliny_data.Command()
        self.options = {
            'letter_csv': [self.letters],
            'people_csv': [self.people]
        }

    def test_read_csv(self):
        command = self.importer
        options = self.options
        letter_list, people_list = command.read_CSVs(**options)

        # output should be a list
        assert isinstance(letter_list, list)
        assert isinstance(people_list, list)
        # there should be two from the fixture
        assert len(letter_list) == 2
        assert len(people_list) == 2

        # All of the fields should be represented
        for field in ["AddresseeID", "Book", "Letter"]:
            assert field in letter_list[0]
        for field in ["ID", "Name", "Gender", "Rank", "Consular", "Uncertain",
                      "Alt.Name", "Notes"]:
            assert field in people_list[0]

    @pytest.mark.usefixtures("pass_capsys")
    def test_make_letters(self):
        command = self.importer
        options = self.options
        letter_list, people_list = command.read_CSVs(**options)

        command.make_letters(letter_list)

        stdout, stderr = self.capsys.readouterr()

        assert "Created: 2 letters" in stdout
        letters = Letter.objects.all()
        assert len(letters) == 2
        assert Letter.objects.get(book=1, letter=5)
        assert Letter.objects.get(book=1, letter=6)

    @pytest.mark.usefixtures("pass_capsys")
    def test_make_people(self):
        command = self.importer
        options = self.options
        letter_list, people_list = command.read_CSVs(**options)

        command.make_letters(letter_list)
        command.make_people(people_list, letter_list)
        stdout, stderr = self.capsys.readouterr()

        assert "Created: 2 people" in stdout
        people = Person.objects.all()
        assert len(people) == 2
        tacitus = people.filter(nomina__icontains='Tacitus')[0]
        assert tacitus.nomina == 'Cornelius Tacitus'
        letters = tacitus.letters_to.all()
        assert len(letters) == 1

        aka = AKA.objects.get(
                person=Person.objects.get(nomina__icontains='Voconius')
            )
        assert isinstance(aka, AKA)
        assert aka.nomina == 'Voconius'
        assert aka.person.nomina == 'Voconius Romanus'    
