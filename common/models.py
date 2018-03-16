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
    first_name = models.CharField(max_length=191, blank=True)
    contributor_type = models.PositiveSmallIntegerField(choices=CONTRIBUTORS)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
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


class Monograph(Work):
    place_of_publication = models.CharField(max_length=191)
    publisher = models.CharField(max_length=191)

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

        bibliography = ('%(author)s, %(title)s in <em>%(book_title)s</em>%(book_translator)s%(book_editor)s (%(book_place)s: %(book_publisher)s, %(book_year)s)' % fields)
        return re.sub(r' +', ' ', bibliography)
