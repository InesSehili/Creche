from django.db import models

# Create your models here.
class Stock(models.Model):
    article = models.CharField(max_length=100 , blank= True , null=True)
    qantite = models.DecimalField(max_digits=30 , blank= True , null=True ,decimal_places =0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)            
