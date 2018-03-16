from django.test import TestCase
from common.models import Article, Contributor, Monograph, Section, Work


class TestContributor(TestCase):

    def test_str(self):
        author1 = Contributor(
            last_name='Author',
            first_name='First',
            contributor_type=Contributor.AUTHOR,
            order=0
        )
        str(author1) == 'First Author'


class TestWork(TestCase):

    def setUp(self):
        self.work = Work.objects.create(
            year=1982,
            title='A Test Work',
        )
        self.author1 = Contributor.objects.create(
            last_name='Author',
            first_name='First',
            contributor_type=Contributor.AUTHOR,
            order=0
        )
        self.author2 = Contributor.objects.create(
            last_name='Author',
            first_name='Second',
            contributor_type=Contributor.AUTHOR,
        )
        self.author3 = Contributor.objects.create(
            last_name='Author',
            first_name='Third',
            contributor_type=Contributor.AUTHOR,
        )
        self.work.contributors.add(self.author1)

    def test_str(self):
        assert str(self.work) == 'A Test Work (1982)'

    def test_contributor_string(self):

        # Basic name handling for 1, 2, and many
        assert self.work._contributor_string(Contributor.AUTHOR) == \
            'First Author'
        self.work.contributors.add(self.author2)
        assert self.work._contributor_string(Contributor.AUTHOR) == \
            'First Author and Second Author'
        self.work.contributors.add(self.author3)
        assert self.work._contributor_string(Contributor.AUTHOR) == \
            'First Author, Second Author, and Third Author'
        self.work.contributors.set([self.author1])
        # Basic prefixing works
        assert self.work._contributor_string(
            Contributor.AUTHOR,
            prefix='trans. ', suffix=', ed.'
        ) == 'trans. First Author, ed.'
        self.work.contributors.add(self.author2)
        assert self.work._contributor_string(
            Contributor.AUTHOR,
            suffix=', ed.'
        ) == 'First Author and Second Author, eds.'


class TestMonograph(TestCase):

    def setUp(self):

        self.author1 = Contributor.objects.create(
            last_name='Author',
            first_name='First',
            contributor_type=Contributor.AUTHOR,
            order=0
        )
        self.author2 = Contributor.objects.create(
            last_name='Author',
            first_name='Second',
            contributor_type=Contributor.AUTHOR,
        )
        self.author3 = Contributor.objects.create(
            last_name='Author',
            first_name='Third',
            contributor_type=Contributor.AUTHOR,
        )
        self.translator1 = Contributor.objects.create(
            last_name='Translator',
            first_name='First',
            contributor_type=Contributor.TRANSLATOR,
            order=0
        )
        self.translator2 = Contributor.objects.create(
            last_name='Translator',
            first_name='Second',
            contributor_type=Contributor.TRANSLATOR,
        )
        self.translator3 = Contributor.objects.create(
            last_name='Translator',
            first_name='Third',
            contributor_type=Contributor.TRANSLATOR,
        )
        self.editor1 = Contributor.objects.create(
            last_name='Editor',
            first_name='First',
            contributor_type=Contributor.EDITOR,
            order=0
        )
        self.editor2 = Contributor.objects.create(
            last_name='Editor',
            first_name='Second',
            contributor_type=Contributor.EDITOR,
        )
        self.editor3 = Contributor.objects.create(
            last_name='Editor',
            first_name='Third',
            contributor_type=Contributor.EDITOR,
        )
        self.test_book = Monograph.objects.create(
            year=1982,
            title='A Test Monograph',
            place_of_publication='London',
            publisher='Foobar University Press'
        )
        self.test_book.contributors.add(self.author1)

    def test_str(self):
        assert str(self.test_book) == 'A Test Monograph (1982)'

    def test_chicago(self):
        # basic book, author
        assert self.test_book.chicago == \
            'First Author, <em>A Test Monograph</em> (London: Foobar University Press, 1982)'
        # book and editor
        self.test_book.contributors.add(self.editor1)
        assert self.test_book.chicago == \
            'First Author, <em>A Test Monograph</em>, ed. First Editor (London: Foobar University Press, 1982)'
        # editor as author
        self.test_book.contributors.set([self.editor1])
        assert self.test_book.chicago == \
            'First Editor, ed., <em>A Test Monograph</em> (London: Foobar University Press, 1982)'
        # multiple editors
        self.test_book.contributors.set([self.editor1, self.editor2])
        assert self.test_book.chicago == \
            'First Editor and Second Editor, eds., <em>A Test Monograph</em> (London: Foobar University Press, 1982)'
        # translator
        self.test_book.contributors.set([self.author1, self.translator1])
        assert self.test_book.chicago == \
            'First Author, <em>A Test Monograph</em>, trans. First Translator (London: Foobar University Press, 1982)'
        # translator as author
        self.test_book.contributors.set([self.translator1])
        assert self.test_book.chicago == \
            'First Translator, trans., <em>A Test Monograph</em> (London: Foobar University Press, 1982)'

        # check citation override
        self.test_book.citation_override = 'Test'
        assert self.test_book.chicago == 'Test'


class TestJournalArticle(TestCase):

    def setUp(self):
        self.author1 = Contributor.objects.create(
            last_name='Author',
            first_name='First',
            contributor_type=Contributor.AUTHOR,
            order=0
        )
        self.author2 = Contributor.objects.create(
            last_name='Author',
            first_name='Second',
            contributor_type=Contributor.AUTHOR,
        )
        self.article = Article.objects.create(
            volume=59,
            year=1972,
            pages='101-102',
            title='A Study of Foo',
            journal='Foo Journal',
            doi_or_url='http://journalstor.org/',
        )
        self.article.contributors.set([self.author1, self.author2])

    def test_str(self):
        assert str(self.article) == "A Study of Foo, Foo Journal (1972)"

    def test_chicago(self):
        assert self.article.chicago == \
            'First Author and Second Author, "A Study of Foo," <em>Foo Journal</em> 59 (1972)'
        # check citation override
        self.article.citation_override = 'Test'
        assert self.article.chicago == 'Test'


class TestSection(TestCase):

    def setUp(self):

        self.author1 = Contributor.objects.create(
            last_name='Author',
            first_name='First',
            contributor_type=Contributor.AUTHOR,
            order=0
        )

        self.translator3 = Contributor.objects.create(
            last_name='Translator',
            first_name='Third',
            contributor_type=Contributor.TRANSLATOR,
        )
        self.editor1 = Contributor.objects.create(
            last_name='Editor',
            first_name='First',
            contributor_type=Contributor.EDITOR,
            order=0
        )

        self.test_book = Monograph.objects.create(
            year=1982,
            title='A Test Monograph',
            place_of_publication='London',
            publisher='Foobar University Press'
        )

        self.test_book.contributors.set([self.translator3, self.editor1])

        self.test_section = Section.objects.create(
            pages='101-124',
            title='A Sample Chapter',
            year=1982,
            contained_in=self.test_book
        )
        self.test_section.contributors.add(self.author1)

    def test_str(self):
        assert str(self.test_section) == \
            'A Sample Chapter in A Test Monograph (1982)'

    def test_chicago(self):
        assert self.test_section.chicago == \
            'First Author, "A Sample Chapter," in <em>A Test Monograph</em>, trans. Third Translator, ed. First Editor (London: Foobar University Press, 1982)'

        # check citation override
        self.test_section.citation_override = 'Test'
        assert self.test_section.chicago == 'Test'
