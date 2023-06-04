from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View, TemplateView
from django.http.response import HttpResponse

class IndexView(TemplateView):
    # a template file name in the templates directory in current application
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        return kwargs