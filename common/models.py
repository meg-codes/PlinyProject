from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re


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
<<<<<<< HEAD
    first_name = models.CharField(max_length=191, blank=True)
=======
    first_name = models.CharField(max_length=191)
>>>>>>> 84605b25484b36dca4d050693c0bf0e7cd86c4f2
    contributor_type = models.PositiveSmallIntegerField(choices=CONTRIBUTORS)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
<<<<<<< HEAD
        return ('%s %s' % (self.first_name, self.last_name)).strip()

    @property
    def last_first(self):
        name = '%s, %s' % (self.last_name, self.first_name)
        if not self.first_name:
            name = name.strip(', ')
        return name


class Work(models.Model):
    contributors = models.ManyToManyField(Contributor)
    year = models.PositiveSmallIntegerField()
    title = models.TextField()
    # in case no particular programmatic setup allows for a display citation
    # in an acceptable format
    citation_override = models.TextField(blank=True)

    def _contributor_string(self, contrib_type, prefix='', suffix=''):
        contributors = list(self.contributors.filter(contributor_type=contrib_type).order_by('order'))
        ret = ''
        plural = False
        if len(contributors) == 0:
            return ret
        if len(contributors) == 1:
            ret = str(contributors[0])
        elif len(contributors) == 2:
            plural = True
            ret = ('%s and %s'
                   % (str(contributors[0]), str(contributors[1])))
        else:
            plural = True
            ret = (
                "%s, %s, and %s" % (str(contributors[0]),
                                    ", ".join(str(contrib)
                                              for contrib in contributors[1:-1]),
                                    str(contributors[-1]))
            )
        if suffix == ', ed.' and plural:
            suffix = ', eds.'

        return '%s%s%s' % (prefix, ret, suffix)

    def __str__(self):
        return self.title
=======
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
>>>>>>> 84605b25484b36dca4d050693c0bf0e7cd86c4f2


class Monograph(Work):
    place_of_publication = models.CharField(max_length=191)
    publisher = models.CharField(max_length=191)

<<<<<<< HEAD
    @property
    def chicago(self):

        fields = {
            'author': self._contributor_string(Contributor.AUTHOR),
            'title': self.title,
            'editor': self._contributor_string(Contributor.EDITOR, prefix=', ed. '),
            'translator': self._contributor_string(Contributor.TRANSLATOR, prefix=', trans. '),
            'place': self.place_of_publication,
            'publisher': self.publisher,
            'year': self.year,
        }

        # - handle editor or translator as author
        if not fields['author']:
            # translator as author
            if fields['translator']:
                fields['author'] = self._contributor_string(Contributor.TRANSLATOR, suffix=', trans.')
                fields['translator'] = ''
            # editor as author
            elif not fields['translator'] and fields['editor']:
                fields['author'] = self._contributor_string(Contributor.EDITOR, suffix=', ed.')
                fields['editor'] = ''

        bibliography = ('%(author)s, <em>%(title)s</em>%(editor)s%(translator)s (%(place)s: %(publisher)s, %(year)s)' %
                        fields)
        bibliography = re.sub(r'(\s,\s+)', ' ', bibliography)
        return re.sub(r' +', ' ', bibliography)


class Article(Work):
    volume = models.PositiveSmallIntegerField()
    pages = models.CharField(max_length=30)
    # this should really be a Work instance, but it complicates things
    # vs. actual use cases
    journal = models.CharField(max_length=191)
    doi_or_url = models.TextField(blank=True)

    @property
    def chicago(self):
        fields = {
            'author': self._contributor_string(Contributor.AUTHOR),
            'title': '"%s,"' % self.title,
            'journal': self.journal,
            'volume': self.volume,
            'year': self.year,
        }
        bibliography = ('%(author)s, %(title)s <em>%(journal)s</em> %(volume)s (%(year)s)' % fields)
        return re.sub(r' +', ' ', bibliography)


class Section(Work):
    pages = models.CharField(max_length=30)
    contained_in = models.ForeignKey(Monograph, related_name='cited_sections')
=======
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
>>>>>>> 84605b25484b36dca4d050693c0bf0e7cd86c4f2

    @property
    def chicago(self):
        fields = {
            'author': self._contributor_string(Contributor.AUTHOR),
            'title': '"%s,"' % self.title,
            'book_editor': self.contained_in._contributor_string(Contributor.EDITOR, prefix=', ed. '),
            'book_translator': self.contained_in._contributor_string(Contributor.TRANSLATOR, prefix=', trans. '),
            'book_title': self.contained_in.title,
            'book_place': self.contained_in.place_of_publication,
            'book_publisher': self.contained_in.publisher,
            'book_year': self.contained_in.year,
        }

<<<<<<< HEAD
        bibliography = ('%(author)s, %(title)s in <em>%(book_title)s</em>%(book_translator)s%(book_editor)s (%(book_place)s: %(book_publisher)s, %(book_year)s)' % fields)
        return re.sub(r' +', ' ', bibliography)
=======
class Section(Work):
    pages = models.Charfield(max_length=30)
>>>>>>> 84605b25484b36dca4d050693c0bf0e7cd86c4f2
