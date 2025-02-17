from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
class HomePageView(TemplateView):
    
    template_name = "pages/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class AboutUsPageView(TemplateView):
    
    template_name = "pages/about.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ServicesPageView(TemplateView):

    template_name = "pages/services.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class TestimonialsPageView(TemplateView):

    template_name = "pages/testimonials.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class BlogPageView(TemplateView):

    template_name = "pages/blog.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class ContactPageView(TemplateView):

    template_name = "pages/contact.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    