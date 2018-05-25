from django.test import TestCase
from django.urls import reverse


class TestContentPage(TestCase):

    def test_get_template(self):

        # test that the template view uses the template requested
        # using pliny as a view that will always be present
        route = reverse('content:render', kwargs={'template': 'pliny'})
        res = self.client.get(route)
        self.assertTemplateUsed(res, 'contentpages/pliny.html')
