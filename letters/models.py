from django.db import models
from prosopography.models import Person


class Letter(models.Model):
    """A letter from one of Pliny's books of personal correspondence"""
    book = models.PositiveSmallIntegerField()
    manuscript_correspondent_name = models.CharField(blank=True, max_length=255)
    letter = models.PositiveSmallIntegerField()
    topics = models.ManyToManyField('Topic', blank=True)
    date = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('book', 'letter')

    def __str__(self):
        value = "%s.%s" % (self.book, self.letter)
        people = Person.objects.filter(letters_to__in=[self])
        if people.exists():
            people_string = ''
            for person in people:
                people_string += "%s, " % person
            value += " to %s" % people_string
        return value.strip(', ')


class Topic(models.Model):
    """A topic for one of Pliny's letters"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
