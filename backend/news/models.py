from django.db import models


class Post(models.Model):
    """Class to holds HTML text formatted blog posts"""
    #: Date that the post is posted
    date_posted = models.DateTimeField(auto_now_add=True)
    #: Date that the post is updated
    date_updated = models.DateTimeField(auto_now=True)
    #: Subject used as the title line of the post
    subject = models.CharField(max_length=255)
    #: Content of the post
    content = models.TextField()

    def __str__(self):
        return '%s - %s' % (self.date_posted, self.subject)

    class Meta:
        ordering = ['-date_posted']
