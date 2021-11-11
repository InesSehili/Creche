from django.db import models
from categoriesAbonnement.models import CategorieAbonnement
from parents.models import Parent
from classes.models import Classe
from supplement.models import Supplement
from autorisations.models import Autorisation
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.timezone import datetime 

# Create your models here.
class Enfant(models.Model) :
    parents = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=100 )
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    age = models.DecimalField(decimal_places =0, max_digits=65, blank=True, null=True,default=0)
    sexe = models.CharField(max_length=32, null=True, blank=True)
    poids =  models.DecimalField(decimal_places =0, max_digits=65, blank=True, null=True,default=0)
    taille =  models.DecimalField(decimal_places =0, max_digits=65, blank=True, null= True ,default=0)
    image = models.FileField(upload_to='enfant/', null=True)
    prix_paye = models.DecimalField(default=0, decimal_places=2, max_digits=65, blank=True, null=True)
    reste_paye = models.DecimalField(default=0, decimal_places=2, max_digits=65, blank=True, null=True) 
    total_payement = models.DecimalField(default=0,decimal_places=2, max_digits=65, blank=True, null=True)  
    autorisation = models.ManyToManyField(Autorisation)
    created_at = models.DateTimeField(default=datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def get_image(self):
        return self.image.url if self.image else static('assets/img/team/default-profile-picture.png')


    



