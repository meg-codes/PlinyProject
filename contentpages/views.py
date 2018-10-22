from django.views.generic import TemplateView


class ContentPage(TemplateView):
    """View for rendering generic content pages"""

    def get_template_names(self):
        if 'template' in self.kwargs:
            return 'contentpages/%s.html' % self.kwargs['template']
