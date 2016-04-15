from __future__ import absolute_import

from celery import shared_task

from documents.models import Document


@shared_task
def compile_tex(document_id):
    document = Document.objects.get(pk=document_id)
    print(document)
