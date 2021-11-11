from django.db import models

# Create your models here.
class Action(models.Model) :
    nom = models.CharField(max_length=100)
    date = models.DateField()
    details = models.TextField(max_length=300)
    frais_action = models.DecimalField(max_digits=70)
    frais_payé = models.DecimalField(max_digits=70)
    
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)    