from django.views.generic import TemplateView

from books.models import Book


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        return {"books": Book.objects.all()}
