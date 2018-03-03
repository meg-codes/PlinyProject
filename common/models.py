from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Contributor(models.Model):
    AUTHOR = 0
    EDITOR = 1
    TRANSLATOR = 2

    CONTRIBUTORS = (
        (AUTHOR, 'Author'),
        (EDITOR, 'Editor'),
        (TRANSLATOR, 'Translator'),
    )

    last_name = models.CharField(max_length=191)
    first_name = models.CharField(max_length=191)
    contributor_type = models.PositiveSmallIntegerField(choices=CONTRIBUTORS)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return ('%s %s' % (self.last_name, self.first_name))


class Work(models.Model):
    contributors = models.ManyToManyField(Contributor, blank=True, null=True)
    year = models.PositiveSmallIntegerField()
    title = models.TextField()
    short_title = models.CharField(max_length=191, db_index=True)
    # in case no particular programmatic setup allows for a display citation
    # in an acceptable format
    citation_override = models.TextField()

    def __str__(self):
        return self.short_title

    def contributor_list(self, contributors):
        if len(contributors) < 4:
            names = []
            for c in contributors:
                names.append('%s %s' % (c.first_name, c.last_name))
            return ', '.join(names)

        else:
            return '%s %s et al.' % (contributors[0].first_name,
                                     contributors[1].last_name)

    def chicago_note(self):
        try:
            instance = self.monograph
            return instance.chicago_note
        except ObjectDoesNotExist:
            pass
        try:
            instance = self.article
            return instance.chicago_note
        except ObjectDoesNotExist:
            pass
        try:
            instance = self.section
            return instance.chicago_note
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("No object that can have a Chicago "
                                     "format string was found.")


class Monograph(Work):
    place_of_publication = models.CharField(max_length=191)
    publisher = models.CharField(max_length=191)

    def chicago(self):

        author_list = ''
        translator_list = ''
        editor_list = ''

        authors = self.contributors.filter(contributor_type=Contributor.AUTHOR)
        editors = self.contributors.filter(contributor_type=Contributor.EDITOR)
        translators = (self.contributors
                       .filter(contributor_type=Contributor.TRANSLATOR))
        if authors.exists():
            author_list = self.contributor_list(authors)
        if translators.exists():
            translator_list = self.contributor_list(translators)
            translator_list += ', trans.'
        if editors.exists():
            editor_list = self.contributor_list(editors)
            len(editors) > 1:
                editor_list += ', eds.'
            else:
                editor_list += ', ed.'

        if not author_list:
            if translator_list:
                author_list = translator_list
                translator_list = ''
            else:
                author_list = editor_list
                editor_list = ''

        return ('%(author_list)s, <em>%(title)s</em>%(trans)s%(ed)s '
                '(%(place)s: %(publisher)s, %(year)s)')




class Article(Work):
    volume = models.PositiveSmallIntegerField()
    # accounts for Summer, Winter, Quarterly, but will also check if it's a
    # standard integer based issue when producing citation
    issue = models.CharField(max_length=5, blank=True)
    pages = models.CharField(max_length=30)
    journal = models.ForeignKey(Work)


class Section(Work):
    pages = models.Charfield(max_length=30)
