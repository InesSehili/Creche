from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Autorisation(models.Model) :
    nom = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    