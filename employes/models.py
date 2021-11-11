from django.db import models
from django.utils.timezone import datetime 


# Create your models here

class Employes(models.Model) :
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=70, unique=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254 ,blank=True , null=True) 
    fonction = models.CharField(max_length=200)
    salaire = models.FloatField()
    id_pointage = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
    created_at = models.DateTimeField(default=datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(auto_now=True)
