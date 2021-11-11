from django.shortcuts import render, redirect
from django.contrib import messages
from supplement.models import Supplement
from supplement.forms import SupplementForm, form_validation_error
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/login/")
def supplement_page(request):
	context = {}

	context['list_supplement'] = Supplement.objects.all().values().order_by("created_at").reverse()
	if request.method =='POST':
		form = SupplementForm(request.POST, request.FILES)
		if form.is_valid():
			print("form is valid")
			form.save()
			messages.success(request, 'Supplement a ete bien ajoute')
			context['list_supplement'] = Supplement.objects.all().values().order_by("created_at").reverse()
		else:
			print("form is not valid")
			messages.error(request,form_validation_error(form))
	return render(request, 'supplement.html', context)

@login_required(login_url="/login/")
def formulaire_modifier_supplement(request):
	context = {}
	
	if request.method == 'POST':
		id_supplement = request.POST.get("id")
		supplement = Supplement.objects.get(id = id_supplement)
		context['supplement'] = supplement
		
	return render(request, 'modifier-supplement.html', context)

@login_required(login_url="/login/")	
def update_supplement(request):
	context = {}
	if request.method == 'POST':
		id_supplement = request.POST.get("id")
		nom = request.POST.get("nom_supplement")
		prix = request.POST.get('prix')
		description = request.POST.get(' description')
		try:
			{Supplement.objects.filter(id =id_supplement).update(nom_supplement=nom)}
		except Exception as e:
			messages.error(request,'nom du supplement existe deja')
			context['list_supplement'] = Supplement.objects.all().values().order_by("created_at").reverse()
			return render(request, 'supplement.html', context)
		
		Supplement.objects.filter(id = id_supplement).update(prix=prix)
		Supplement.objects.filter(id = id_supplement).update(description=description)
		messages.info(request, 'Supplement a ete bien modifie')

	context['list_supplement'] = Supplement.objects.all().values().order_by("created_at").reverse()
	return render(request, 'supplement.html', context)
@login_required(login_url="/login/")
def delete_supplement(request):
	context = {}
	if request.method == 'POST':
		id_supplement = request.POST.get("id")
		try:
			supplement = Supplement.objects.get(id = id_supplement)
			supplement.delete()
		except Exception as e:
			print("")

		
		
	messages.info(request, 'Supplement a ete bien supprimé')
	context['list_supplement'] = Supplement.objects.all().values().order_by("created_at").reverse()
	return render(request, 'supplement.html', context)







