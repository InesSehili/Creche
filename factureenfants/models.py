from django.db import models
from enfants.models import Enfant
from categoriesAbonnement.models import CategorieAbonnement
from supplement.models import Supplement
from autorisations.models import Autorisation


# Create your models here.
class FactureEnfant(models.Model) :
	enfant =models.ForeignKey(Enfant , on_delete=models.CASCADE , null= True , blank=True)
	supplement = models.ManyToManyField(Supplement)
	
	categorie = models.ForeignKey(CategorieAbonnement, on_delete=models.CASCADE)
	client = models.CharField(blank=True , null=True, max_length=60)
	frais_inscription =  models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
	prix_total = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
	prix_paye = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
	reste_paye = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



	


