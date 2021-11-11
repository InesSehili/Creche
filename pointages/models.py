from django.db import models
from employes.models import Employes
from enfants.models import Enfant

# Create your models here.

class Pointage(models.Model) :
    employe = models.ForeignKey(Employes, on_delete=models.CASCADE, null=True, blank=True)
    enfant = models.ForeignKey(Enfant, on_delete=models.CASCADE, null=True, blank=True)
    date_pointage = models.DateTimeField(blank=True ,null=True)
    raison_pointage = models.CharField(max_length=32, null=True, blank=True) 
   
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


