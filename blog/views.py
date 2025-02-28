from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
class BlogPageView(TemplateView):

    template_name = "pages/blog.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

