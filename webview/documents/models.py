from django.db import models
from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    if not value.name.endswith('.zip'):
        raise ValidationError(u"The file extension isn't zip.")
    return True

# Create your models here.
class Document(models.Model):
    STATES = (
                ('E', 'Erreur'),
                ('D', 'Done'),
                ('W', 'Waiting'),
            )
    titre = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATES, default='W', db_index=True, verbose_name='État')
    zipFile = models.FileField(upload_to="uploads/", validators=[validate_file_extension])
    pdf = models.FileField(upload_to="pdf/", blank=True, null=True)
    clean = models.BooleanField(default=False)

    def __repr__(self):
        return "<Document: '%s'>" % self.titre

    def __str__(self):
        return self.titre

    def filename(self):
        return os.path.basename(self.zipFile.name)
