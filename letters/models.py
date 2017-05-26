from django.db import models


class Letter(models.Model):
    """A letter from one of Pliny's books of personal correspondence"""
    book = models.PositiveSmallIntegerField()
    letter = models.PositiveSmallIntegerField()
    topic = models.ManyToManyField('Topic')
    date = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('book', 'letter')


class Topic(models.Model):
    """A topic for one of Pliny's letters"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
