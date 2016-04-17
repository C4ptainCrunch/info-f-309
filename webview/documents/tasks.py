from __future__ import absolute_import

from celery import shared_task

from documents.models import Document
import clamd


@shared_task
def compile_tex(document_id):
    document = Document.objects.get(pk=document_id)
    print(document)


@shared_task
def check_clamav(document_id):
    document = Document.objects.get(pk=document_id)
    clam = clamd.ClamdUnixSocket(settings.CLAMAV_SOCKET)
    status, sig = clam.scan(absolute_path_to_pdf)[absolute_path_to_pdf]
    if status == 'OK':
        document.isClean = True
    elif status == 'FOUND':
        document.isClean = False
        print("Signature found", sig)
    else:
        # unknown state
       document.isClean = False
       print("Unknown return of clamav", status, sig)

    document.save()


