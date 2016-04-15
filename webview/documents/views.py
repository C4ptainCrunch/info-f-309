from django.shortcuts import render
from django.views import generic
from .models import Document
from django import forms

from documents import tasks


# Create your views here.
class ListView(generic.ListView):
    template_name = 'documents/index.html'
    model = Document
    context_object_name = 'documents_list'

class UploadFormView(generic.edit.CreateView):
    model = Document
    fields = ['titre', 'zipFile']
    success_url = '/'

    def form_valid(self, form):
        ret = super(UploadFormView, self).form_valid(form)
        tasks.compile_tex.delay(self.object.id)
        return ret
