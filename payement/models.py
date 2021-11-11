from django.db import models
from factureenfants.models import FactureEnfant
from django.core.validators import MinValueValidator
from decimal import Decimal
from enfants.models import Enfant 
# Create your models here.
class Payement(models.Model):
	enfant = models.ForeignKey(Enfant, on_delete=models.CASCADE, null=True, blank=True)
	facture = models.ForeignKey(FactureEnfant, on_delete=models.CASCADE, null=True, blank=True)
	prix_payer = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0, validators=[MinValueValidator(Decimal('0.01'))])
	reste_facture_apres_ce_paiment = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
	client = models.CharField(max_length=32, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	