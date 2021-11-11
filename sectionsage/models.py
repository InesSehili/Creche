from django.db import models

# Create your models here.
class SectionAge(models.Model):
	section_age1 = models.DecimalField(decimal_places=0, max_digits=65, blank=True, default=0)
	section_age2 = models.DecimalField(decimal_places=0, max_digits=65, blank=True, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
