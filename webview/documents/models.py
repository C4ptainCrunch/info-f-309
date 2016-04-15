from django.db import models
import os

# Create your models here.
class Document(models.Model):
    STATES = (
                ('E', 'Erreur'),
                ('D', 'Done'),
                ('W', 'Waiting'),
            )
    titre = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATES, default='W', db_index=True, verbose_name='État')
    zipFile = models.FileField(upload_to="uploads/", blank=True, null=True)
    pdf = models.FileField(upload_to="pdf/", blank=True, null=True)

    def __repr__(self):
        return "<Document: '%s'>" % self.titre

    def __str__(self):
        return self.titre

    def filename(self):
        return os.path.basename(self.zipFile.name)
