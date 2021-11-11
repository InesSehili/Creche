from django import forms 
from payement.models import Payement

class PaymentForm(forms.ModelForm):


	class Meta:
		model = Payement
		fields = '__all__'

def form_validation_error(form):
	msg = ""
	for field in form:
		for error in field.errors:
			msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
		return msg