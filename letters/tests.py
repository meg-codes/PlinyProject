from django.test import TestCase

from prosopography.models import Correspondent
from .models import Letter, Topic


class TestLetter(TestCase):

    def setUp(self):
        self.quintus = Correspondent.objects.create(**{
            'nomina': 'Quintus',
            'gender': 'M',
        })

        self.quinta = Correspondent.objects.create(**{
            'nomina': 'Quinta',
            'gender': 'F',
        })

        self.topic = Topic.objects.create(name='disiecta membra')

    def test_str(self):
        letter = Letter.objects.create(**{
            'book': 5,
            'letter': 12
        })

        assert str(letter) == "5.12"
        letter.letters_to.add(self.quintus)
        assert str(letter) == "5.12 to Quintus"
        letter.letters_to.add(self.quinta)
        assert str(letter) == "5.12 to Quintus, Quinta"

    def test_add_topic(self):
        letter = Letter.objects.create(**{
            'book': 5,
            'letter': 12
        })

        letter.topics.add(self.topic)
        assert letter.topics.count() == 1
        assert letter.topics.first().name == 'disiecta membra'


class TestTopic(TestCase):

    def test_str(self):
        topic = Topic(name='foo')
        assert str(topic) == 'foo'
