from django.core.exceptions import ValidationError
from django.test import TestCase
import pytest

from common.models import Article, Citation, Contributor, Monograph, Section, \
                          Work, WorkContributor


class TestContributor(TestCase):

    def test_str(self):
        author1 = Contributor(
            last_name='Author',
            first_name='First',
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
        )
        self.author2 = Contributor.objects.create(
            last_name='Author',
            first_name='Second',
        )
        self.author3 = Contributor.objects.create(
            last_name='Author',
            first_name='Third',
        )
        WorkContributor.objects.create(
            work=self.work,
            contributor=self.author1,
            contribution_type=WorkContributor.AUTHOR,
            order=0
        )

    def test_str(self):
        assert str(self.work) == 'A Test Work (1982)'

    def test_contributor_string(self):

        # Basic name handling for 1, 2, and many
        assert self.work._contributor_string(WorkContributor.AUTHOR) == \
            'First Author'
        WorkContributor.objects.create(
            work=self.work,
            contributor=self.author2,
            contribution_type=WorkContributor.AUTHOR,
            order=1
        )
        assert self.work._contributor_string(WorkContributor.AUTHOR) == \
            'First Author and Second Author'
        WorkContributor.objects.create(
            work=self.work,
            contributor=self.author3,
            contribution_type=WorkContributor.AUTHOR,
            order=2
        )
        assert self.work._contributor_string(WorkContributor.AUTHOR) == \
            'First Author, Second Author, and Third Author'
        WorkContributor.objects.\
            filter(contributor__in=[self.author2, self.author3])\
            .delete()
        # Basic prefixing work
        assert self.work._contributor_string(
            WorkContributor.AUTHOR,
            prefix='trans. ', suffix=', ed.'
        ) == 'trans. First Author, ed.'
        WorkContributor.objects.create(
            work=self.work,
            contributor=self.author2,
            contribution_type=WorkContributor.AUTHOR,
            order=1
        )
        assert self.work._contributor_string(
            WorkContributor.AUTHOR,
            suffix=', ed.'
        ) == 'First Author and Second Author, eds.'


class TestMonograph(TestCase):

    def setUp(self):

        self.author1 = Contributor.objects.create(
            last_name='Author',
            first_name='First',
        )
        self.author2 = Contributor.objects.create(
            last_name='Author',
            first_name='Second',
        )
        self.author3 = Contributor.objects.create(
            last_name='Author',
            first_name='Third',
        )
        self.translator1 = Contributor.objects.create(
            last_name='Translator',
            first_name='First',
        )
        self.translator2 = Contributor.objects.create(
            last_name='Translator',
            first_name='Second',
        )
        self.translator3 = Contributor.objects.create(
            last_name='Translator',
            first_name='Third',
        )
        self.editor1 = Contributor.objects.create(
            last_name='Editor',
            first_name='First',
        )
        self.editor2 = Contributor.objects.create(
            last_name='Editor',
            first_name='Second',
        )
        self.editor3 = Contributor.objects.create(
            last_name='Editor',
            first_name='Third',
        )
        self.test_book = Monograph.objects.create(
            year=1982,
            title='A Test Monograph',
            place_of_publication='London',
            publisher='Foobar University Press'
        )

    def test_str(self):
        assert str(self.test_book) == 'A Test Monograph (1982)'

    def test_chicago(self):
        # basic book, author
        first_auth = WorkContributor.objects.create(
            contributor=self.author1,
            work=self.test_book,
            contribution_type=WorkContributor.AUTHOR,
            order=0
        )
        assert self.test_book.chicago == \
            'First Author, <em>A Test Monograph</em> (London: Foobar University Press, 1982)'
        # book and editor
        edit1 = WorkContributor.objects.create(
            contributor=self.editor1,
            work=self.test_book,
            contribution_type=WorkContributor.EDITOR,
            order=0
        )
        assert self.test_book.chicago == \
            'First Author, <em>A Test Monograph</em>, ed. First Editor (London: Foobar University Press, 1982)'
        first_auth.delete()
        # editor as author
        assert self.test_book.chicago == \
            'First Editor, ed., <em>A Test Monograph</em> (London: Foobar University Press, 1982)'
        # multiple editors
        edit2 = WorkContributor.objects.create(
            contributor=self.editor2,
            work=self.test_book,
            contribution_type=WorkContributor.EDITOR,
            order=1
        )
        assert self.test_book.chicago == \
            'First Editor and Second Editor, eds., <em>A Test Monograph</em> (London: Foobar University Press, 1982)'
        edit1.delete()
        edit2.delete()

        # translator
        first_auth = WorkContributor.objects.create(
            contributor=self.author1,
            work=self.test_book,
            contribution_type=WorkContributor.AUTHOR,
            order=0
        )
        translator = WorkContributor.objects.create(
            contributor=self.translator1,
            work=self.test_book,
            contribution_type=WorkContributor.TRANSLATOR,
            order=0
        )
        assert self.test_book.chicago == \
            'First Author, <em>A Test Monograph</em>, trans. First Translator (London: Foobar University Press, 1982)'
        # translator as author
        first_auth.delete()
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
        )
        self.author2 = Contributor.objects.create(
            last_name='Author',
            first_name='Second',
        )
        self.article = Article.objects.create(
            volume=59,
            year=1972,
            pages='101-102',
            title='A Study of Foo',
            journal='Foo Journal',
            doi_or_url='http://journalstor.org/',
        )

        WorkContributor.objects.create(
            work=self.article,
            contributor=self.author2,
            contribution_type=WorkContributor.AUTHOR,
            order=1
        )
        
        WorkContributor.objects.create(
            work=self.article,
            contributor=self.author1,
            contribution_type=WorkContributor.AUTHOR,
            order=0
        )



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

        )

        self.translator3 = Contributor.objects.create(
            last_name='Translator',
            first_name='Third',
        )
        self.editor1 = Contributor.objects.create(
            last_name='Editor',
            first_name='First',
        )

        self.test_book = Monograph.objects.create(
            year=1982,
            title='A Test Monograph',
            place_of_publication='London',
            publisher='Foobar University Press'
        )

        WorkContributor.objects.create(
            work=self.test_book,
            contributor=self.editor1,
            contribution_type=WorkContributor.EDITOR,
            order=0
        )
        WorkContributor.objects.create(
            work=self.test_book,
            contributor=self.translator3,
            contribution_type=WorkContributor.TRANSLATOR,
            order=0
        )


        self.test_section = Section.objects.create(
            pages='101-124',
            title='A Sample Chapter',
            year=1982,
            contained_in=self.test_book
        )

        WorkContributor.objects.create(
            work=self.test_section,
            contributor=self.author1,
            contribution_type=WorkContributor.AUTHOR,
            order=0
        )

    def test_str(self):
        assert str(self.test_section) == \
            'A Sample Chapter in A Test Monograph (1982)'

    def test_chicago(self):
        assert self.test_section.chicago == \
            'First Author, "A Sample Chapter," in <em>A Test Monograph</em>, trans. Third Translator, ed. First Editor (London: Foobar University Press, 1982)'

        # check citation override
        self.test_section.citation_override = 'Test'
        assert self.test_section.chicago == 'Test'


class TestCitation(TestCase):

    def setUp(self):

        self.test_book = Monograph.objects.create(
            year=1982,
            title='A Test Monograph',
            place_of_publication='London',
            publisher='Foobar University Press'
        )

        self.article = Article.objects.create(
            volume=59,
            year=1972,
            pages='101-102',
            title='A Study of Foo',
            journal='Foo Journal',
            doi_or_url='http://journalstor.org/',
        )

    def test_str(self):
        cite = Citation(monograph=self.test_book, pages='123')
        assert str(cite) == \
            'A Test Monograph (1982): 123'

    def test_clean(self):

        cite = Citation(monograph=self.test_book, pages='123-456')
        # clean should not raise an error
        cite.clean()
        cite.article = self.article
        # clean should raise an error because of two citations
        with pytest.raises(ValidationError):
            cite.clean()

    def test_chicago(self):
        cite = Citation(monograph=self.test_book, pages='123-456')
        assert cite.chicago == \
            '<em>A Test Monograph</em> (London: Foobar University Press, 1982), 123-456.'

        cite = Citation(article=self.article, pages='456-789')
        assert cite.chicago == \
            '"A Study of Foo," <em>Foo Journal</em> 59 (1972): 456-789.'
