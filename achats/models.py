from django.db import models

from stock.models import Stock

# Create your models here.

class Achat(models.Model):
     date = models.DateField(null=True, blank=True)
     prix = models.DecimalField(max_digits=65 ,null=True, blank=True ,decimal_places =0)
     article = models.ManyToManyField(Stock)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)