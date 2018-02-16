from django.db import models


class ScholarlyWork(models.Model):
    """Any scholarly work, with a relatively imprecise full text field."""
    short_ref = models.CharField(max_length=255)
    bib_reference = models.TextField()
    year = models.PositiveSmallIntegerField()


class Citation(models.Model):
    """A citation to a particular work."""
    page_section_reference = models.CharField(max_length=255)
    scholarly_work = models.ForeignKey(ScholarlyWork)
