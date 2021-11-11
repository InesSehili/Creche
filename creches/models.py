from django.db import models
from django.utils.translation import gettext as _
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your models here.
class Creche(models.Model):
	nom = models.CharField(max_length=100)
	telephone1 = models.CharField(max_length=32, null=True, blank=True)
	telephone2 = models.CharField(max_length=32, null=True, blank=True)
	email = models.EmailField(max_length=254,null=True, blank=True)
	adresse = models.CharField(max_length=255, null=True, blank=True)
	image = models.FileField(upload_to='creche/', null=True, blank=True)
	gerant = models.CharField(max_length=255, null=True, blank=True)
	nif = models.CharField(max_length=255, null=True, blank=True)
	rc = models.CharField(max_length=255, null=True, blank=True)



	@property
	def get_image(self):
		return self.image.url if self.image else static('assets/img/team/default-profile-picture.png')

   