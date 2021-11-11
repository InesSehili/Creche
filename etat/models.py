from django.db import models
from autorisations.models import Autorisation
from enfants.models import Enfant

# Create your models here.
class Etat(models.Model):
	enfant = models.ForeignKey(Enfant, on_delete=models.CASCADE, null=True, blank=True)
	autorisation = models.ForeignKey(Autorisation, on_delete=models.CASCADE, null=True, blank=True)
	statuts =  models.BooleanField(default=False, null=True, blank=True)
