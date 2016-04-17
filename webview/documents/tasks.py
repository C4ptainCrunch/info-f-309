from __future__ import absolute_import

from celery import shared_task

from documents.models import Document
from django.conf import settings
from django.core.files import File
import clamd
import os
import subprocess


@shared_task
def compile_tex(document_id):
    print("compiling")
    script = os.path.join(settings.BASE_DIR, '../scripts', 'jailifier.sh')
    document = Document.objects.get(pk=document_id)
    command = ["sh", script, str(document.id), document.zipFile.path]
    fout = open("/tmp/compile-%d.stdout" % document.id, "w")
    ferr = open("/tmp/compile-%d.stderr" % document.id, "w")
    try:
        subprocess.check_call(command, timeout=1800, stdout=fout, stderr=ferr)
        f = File(open("/tmp/%d.pdf" % document.id, "rb"), 'rb')
        document.pdf.save(document.titre + ".pdf", f)
        os.remove("/tmp/%d.pdf" % document.id)
        document.status = "D"
        document.save()
    except subprocess.CalledProcessError as e:
        print(e)
        document.status = "E"
        document.save()


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


