from django.db import models
from employes.models import Employes
from enfants.models import Enfant
from decimal import Decimal
from django.core.validators import MinValueValidator
# Create your models here.
class Facture(models.Model) :
    enfant =models.ForeignKey(Enfant , on_delete=models.CASCADE , null= True , blank=True)
    employe = models.ForeignKey(Employes, on_delete=models.CASCADE, null=True, blank=True)
    mois = models.CharField(blank=True , null=True ,max_length=60)
    date =models.DateField(null=True, blank=True)
    tarif = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0 ,validators=[MinValueValidator(Decimal('0.00'))])
    client = models.CharField(blank=True , null=True, max_length=60)
    les_jours = models.CharField(blank=True , null=True , max_length=200)
    personne_concernee=models.CharField(blank=True , null=True , max_length=60)
    frais_inscription = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0 , validators=[MinValueValidator(Decimal('0.00'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
      

