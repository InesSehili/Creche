from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Supplement(models.Model) :
    nom_supplement = models.CharField(max_length=100, unique=True)
    prix = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    