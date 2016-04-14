from django.db import models

# Create your models here.
class Document(models.Model):
    STATES = (
                ('E', 'Erreur'),
                ('D', 'Done'),
                ('W', 'Waiting'),
            )
    titre = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATES, default='PREPARING', db_index=True, verbose_name='État')
    zipFile = models.FileField(upload_to="uploads/", blank=True, null=True)
    pdf = models.FileField(upload_to="pdf/", blank=True, null=True)

    def __str__(self):
        return self.titre
