from django.db import models

class Parent(models.Model) :
    pere = models.CharField(max_length=100)
    mere = models.CharField(max_length=100)
    adresse = models.CharField(max_length=500)
    wilaya = models.CharField(max_length=100)
    telephone_pere = models.CharField(max_length=200)
    telephone_mere = models.CharField(max_length=200)
    etat = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    personne_autorise = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    
