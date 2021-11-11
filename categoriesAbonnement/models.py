from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from sectionsage.models import SectionAge

class CategorieAbonnement(models.Model) :
	nom = models.CharField(max_length=100)
	prix = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0, validators=[MinValueValidator(Decimal('0.00'))])
	description = models.TextField(blank=True, null=True)
	section_age = models.ForeignKey(SectionAge, on_delete=models.CASCADE)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)



