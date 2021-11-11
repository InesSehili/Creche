from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Depense(models.Model) :
	nom = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)
