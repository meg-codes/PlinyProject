import csv

# django modules
from django.core.management.base import BaseCommand, CommandError


# local imports
from letters.models import Letter
from prosopography.models import AKA, Person

csv.register_dialect('mysqlcsv', delimiter=';')


class Command(BaseCommand):
    help = 'Import letters and people csv files'

    def add_arguments(self, parser):
        parser.add_argument('letter_csv', type=str, nargs=1)
        parser.add_argument('people_csv', type=str, nargs=1)

    def read_CSVs(self, **options):
        letter_list = []
        people_list = []
        """Read and return the CSVs as lists of dicts"""
        with open(options['letter_csv'][0], 'r') as old_letters:
            reader = csv.DictReader(old_letters, dialect='mysqlcsv')
            try:
                for letter in reader:
                    letter_list.append(letter)
            except csv.Error as e:
                self.stdout.write(e)

            if not letter_list[0]['Book']:
                letter_list = "This does not look like a letters csv"

        with open(options['people_csv'][0], 'r') as old_people:
            reader = csv.DictReader(old_people, dialect='mysqlcsv')
            try:
                for person in reader:
                    people_list.append(person)
            except csv.Error as e:
                self.stdout.write(e)
            if not people_list[0]['Name']:
                people_list = "This does not look like a people csv"

        return letter_list, people_list

    def make_letters(self, letter_list):
        letter_count = 0
        for letter in letter_list:
            Letter.objects.create(
                book=letter['Book'],
                letter=letter['Letter'],
            )
            letter_count += 1

        self.stdout.write('Created: %s letters' % letter_count)

    def make_people(self, people_list, letter_list):
        person_count = 0
        for person in people_list:
            # Easy fields
            person_dict = {
                'nomina': person['Name'],
                'gender': person['Gender'],
                'notes': person['Notes'],
            }

            # handle the class settings
            possible_old_types = {
                'Senatorial': ['Y', 'Y', 'Y'],
                'Equestrian': ['Y', 'Y', 'N'],
                'Roman Citizen': ['Y', 'N', 'N', 'N']
            }

            i = 0
            for field in ['citizen', 'equestrian', 'senatorial']:
                    person_dict[field] = possible_old_types[person['Rank']][i]
                    i += 1

            # Add the consular flag
            if person['Consular'] == 'Yes':
                person_dict['consular'] = 'Y'

            # Add the certainty flag
            if person['Uncertain'] == 'Yes':
                person_dict['certainty_of_id'] = 1

            # Save and make the person
            person_obj = Person.objects.create(**person_dict)

            # Add the letters to the person
            for letter in letter_list:
                if letter['AddresseeID'] == person['ID']:
                    letter_obj = Letter.objects.get(
                        book=letter['Book'],
                        letter=letter['Letter'])
                    person_obj.letters_to.add(letter_obj)

            person_count += 1

        return self.stdout.write('Created: %s people' % person_count)

    def handle(self, *args, **options):

        # read the CSVs and return error strings to break
        letter_list, people_list = self.read_CSVs(options)

        if isinstance(letter_list, str):
            return self.stdout.write(letter_list)
        if isinstance(people_list, str):
            return self.stdout.write(people_list)
        # make letters
        self.make_letters(letter_list)
        # make people
        self.make_people(people_list, letter_list)
