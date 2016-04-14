from django.shortcuts import render
from django.views import generic
from .models import Document

# Create your views here.
class ListView(generic.ListView):
    template_name = 'documents/index.html'
    model = Document
    context_object_name = 'documents_list'
