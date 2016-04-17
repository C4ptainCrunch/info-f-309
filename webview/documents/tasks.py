from __future__ import absolute_import

from celery import shared_task

from documents.models import Document
from django.conf import settings
import clamd
import os
import subprocess


@shared_task
def compile_tex(document_id):
    script = os.path.join(settings.BASE_DIR, '../scripts', 'jailifier.sh')
    document = Document.objects.get(pk=document_id)
    command = ["sh", script, document.id, document.zipFile.path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1800, check=True)


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


