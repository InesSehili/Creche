from django.shortcuts import render, redirect
from django.contrib import messages
from categoriesAbonnement.models import CategorieAbonnement
from categoriesAbonnement.forms import CategorieForm, form_validation_error
from sectionsage.models import SectionAge
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/login/")
def categorie_abonnement_page(request):
	context = {}

	context['list_categorie_abonement'] = CategorieAbonnement.objects.all().order_by("created_at").reverse()
	context['list_section_age'] = SectionAge.objects.all()
	if request.method =='POST':
		form = CategorieForm(request.POST, request.FILES)
		if form.is_valid():
			print("form is valid")
			form.save()
			messages.success(request, 'Catégorie a été bien ajouté')
			context['list_categorie_abonement'] = CategorieAbonnement.objects.all().order_by("created_at").reverse()
		else:
			print("form is not valid")
			messages.error(request,form_validation_error(form))
	return render(request, 'categorie-abonnement.html', context)

@login_required(login_url="/login/")
def formulaire_modifier_categorie_abonnement(request):
	context = {}
	
	if request.method == 'POST':
		id_categorie_abonnement = request.POST.get("id")
		categorie = CategorieAbonnement.objects.get(id = id_categorie_abonnement)
		context['list_section_age'] = SectionAge.objects.all()
		context['categorie'] = categorie
		
	return render(request, 'modifier-categorie.html', context)

@login_required(login_url="/login/")	
def update_categori_abonnement(request):
	context = {}
	if request.method == 'POST':
		id_categorie_abonnement = request.POST.get("id")
		nom = request.POST.get("nom")
		prix = request.POST.get('prix')
		description = request.POST.get('description')
		id_section_age = request.POST.get('section_age')
		section_age = SectionAge.objects.get(id = id_section_age) 
		
		CategorieAbonnement.objects.filter(id =id_categorie_abonnement).update(nom=nom)

		
		CategorieAbonnement.objects.filter(id = id_categorie_abonnement).update(prix=prix)
		CategorieAbonnement.objects.filter(id = id_categorie_abonnement).update(description=description)
		CategorieAbonnement.objects.filter(id = id_categorie_abonnement).update(section_age=section_age)

		messages.info(request, 'Catégorie a été bien modifie')
	context['list_section_age'] = SectionAge.objects.all()
	context['list_categorie_abonement'] = CategorieAbonnement.objects.all().order_by("created_at").reverse()
	return render(request, 'categorie-abonnement.html', context)
@login_required(login_url="/login/")
def delete_categorie_abonnement(request):
	context = {}
	if request.method == 'POST':
		id_categorie_abonnement = request.POST.get("id")
		categorie = CategorieAbonnement.objects.get(id = id_categorie_abonnement)
		categorie.delete()
	messages.info(request, 'Catégorie a été bien supprimé')
	context['list_categorie_abonement'] = CategorieAbonnement.objects.all().order_by("created_at").reverse()
	context['list_section_age'] = SectionAge.objects.all()
	return render(request, 'categorie-abonnement.html', context)







