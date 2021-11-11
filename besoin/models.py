from django.db import models

# Create your models here.
class Besoin(models.Model):
    date = models.DateField(blank= True , null=True)
    note =models.CharField(max_length=100 , blank= True , null=True )
    article = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        
