from datetime import date
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from factures.models import Facture
from achats.models import Achat
from stock.models import Stock

# Create your models here.
class Prixsortie(models.Model):
	prix_sortie = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0, validators=[MinValueValidator(Decimal('0.00'))])
	created_at = models.DateTimeField(auto_now_add=True)
	article = models.CharField(blank=True , null=True , max_length=200)
	date =models.DateField(null=True, blank=True)
	facture = models.ForeignKey(Facture, on_delete=models.CASCADE , null= True , blank=True)
	updated_at = models.DateTimeField(auto_now=True)
	raison_payement =  models.CharField(max_length=32, null=True, blank=True)
	
