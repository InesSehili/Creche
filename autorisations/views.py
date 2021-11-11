from django.shortcuts import render, redirect
from django.contrib import messages
from autorisations.models import  Autorisation
from autorisations.forms import AutorisationForm, form_validation_error
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/login/")
def autorisation_page(request):
	context = {}

	context['list_autorisation'] = Autorisation.objects.all().values().order_by("created_at").reverse()
	if request.method =='POST':
		form = AutorisationForm(request.POST, request.FILES)
		if form.is_valid():
			print("form is valid")
			form.save()
			messages.success(request, 'Autorisation a été bien ajouté')
			context['autorisation_abonement'] = Autorisation.objects.all().values().order_by("created_at").reverse()
		else:
			print("form is not valid")
			messages.error(request,form_validation_error(form))
	return render(request, 'autorisation.html', context)

@login_required(login_url="/login/")
def formulaire_modifier_autorisation(request):
	context = {}
	
	if request.method == 'POST':
		id_autorisation = request.POST.get("id")
		autorisation = Autorisation.objects.get(id = id_autorisation)
		context['autorisation'] = autorisation
		
	return render(request, 'modifier-autorisatio.html', context)

@login_required(login_url="/login/")	
def update_autorisation(request):
	context = {}
	if request.method == 'POST':
		nom = request.POST.get("nom")
		id_autorisation = request.POST.get("id")
		try:
			{Autorisation.objects.filter(id =id_autorisation).update(nom=nom)}
		except Exception as e:
			print(e)
			messages.error(request,'Autorisation existe déja')
			context['list_autorisation'] = Autorisation.objects.all().values().order_by("created_at").reverse()
			return render(request, 'autorisation.html', context)
		
		
		messages.info(request, 'Autorisation a été bien modifié')

	context['list_autorisation'] = Autorisation.objects.all().values().order_by("created_at").reverse()
	return render(request, 'autorisation.html', context)
@login_required(login_url="/login/")
def delete_autorisation(request):
	context = {}
	if request.method == 'POST':
		id_autorisation = request.POST.get("id")
		autorisation = Autorisation.objects.get(id = id_autorisation)
		autorisation.delete()
	messages.info(request, 'Autorisation a été bien supprimé')
	context['list_autorisation'] = Autorisation.objects.all().values().order_by("created_at").reverse()
	return render(request, 'autorisation.html', context)







