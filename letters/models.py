from django.db import models
from common.models import Citation


class Letter(models.Model):
    """A letter from one of Pliny's books of personal correspondence"""
    book = models.PositiveSmallIntegerField()
    manuscript_correspondent_name = models.CharField(blank=True, max_length=255)
    letter = models.PositiveSmallIntegerField()
    topics = models.ManyToManyField('Topic', blank=True)
    date = models.PositiveSmallIntegerField(blank=True, null=True)
    citations = models.ManyToManyField(Citation, blank=True)

    class Meta:
        unique_together = ('book', 'letter')
        ordering = ['book', 'letter']

    def __str__(self):
        return "%s.%s" % (self.book, self.letter)


class Topic(models.Model):
    """A topic for one of Pliny's letters"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
