from __future__ import absolute_import

from celery import shared_task

from documents.models import Document
from django.conf import settings
from django.core.files import File
import clamd
import os
import subprocess
import re


@shared_task
def compile_tex(document_id):
    print("compiling")
    script = os.path.join(settings.BASE_DIR, '../scripts', 'jailifier.sh')
    document = Document.objects.get(pk=document_id)
    command = ["sh", script, str(document.id), document.zipFile.path]
    fout = open("/var/log/celery/compilation/compile-%d.stdout" % document.id, "w")
    ferr = open("/var/log/celery/compilation/compile-%d.stderr" % document.id, "w")
    try:
        subprocess.check_call(command, timeout=1800, stdout=fout, stderr=ferr)
        f = File(open("/tmp/compile/%d.pdf" % document.id, "rb"), 'rb')
        name = re.sub('[^A-Za-z0-9_]', '', document.titre.replace(" ", "_")) + ".pdf"
        document.pdf.save(name, f)
        os.remove("/tmp/compile/%d.pdf" % document.id)
        document.status = "D"
        document.save()
        check_clamav.delay(document_id)
    except subprocess.CalledProcessError as e:
        print(e)
        document.status = "E"
        document.save()


@shared_task
def check_clamav(document_id):
    document = Document.objects.get(pk=document_id)
    clam = clamd.ClamdUnixSocket(settings.CLAMAV_SOCKET)
    status, sig = clam.scan(document.pdf.path)[document.pdf.path]
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


