from django.db import models

# Create your models here.
class Contrat(models.Model) :
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_contrat = models.DateField()



created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)

