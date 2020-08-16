import os

import pytest
from django.conf import settings
from django.test import TestCase

from prosopography.management.commands import import_pliny_data
from prosopography.models import AKA, Person
from letters.models import Letter

FIXTURES_DIR = os.path.join(settings.BASE_DIR, 'prosopography', 'fixtures')


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
        voconius = people.filter(nomina__icontains='Voconius')[0]
        assert tacitus.nomina == 'Cornelius Tacitus'
        letters = tacitus.letters_to.all()
        assert len(letters) == 1
        assert tacitus.citizen == 'Y'
        assert tacitus.equestrian == 'N'
        assert tacitus.consular == 'Y'
        assert tacitus.certainty_of_id == 5
        assert voconius.certainty_of_id == 1

        aka = AKA.objects.get(person=voconius)
        assert isinstance(aka, AKA)
        assert aka.nomina == 'Voconius'
        assert aka.person.nomina == 'Voconius Romanus'
