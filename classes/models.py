from django.db import models

from employes.models import Employes

# Create your models here.
class Classe(models.Model):

    employe = models.ForeignKey(Employes, on_delete=models.SET_NULL ,null=True ,blank= True )


    nom_classe = models.CharField(max_length=200)
    niveau = models.TextField(max_length=300)
    nbr_enfant = models.DecimalField(decimal_places =0,max_digits=20 , null=True ,blank= True , default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    