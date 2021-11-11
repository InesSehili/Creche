from django.shortcuts import render, redirect
from django.contrib import messages
from sectionsage.models import  SectionAge
from sectionsage.forms import SectionAgeForm, form_validation_error
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/login/")
def section_age_page(request):
	context = {}

	context['list_section_age'] = SectionAge.objects.all().values().order_by("created_at").reverse()
	if request.method =='POST':
		form = SectionAgeForm(request.POST, request.FILES)
		if form.is_valid():
			print("form is valid")
			form.save()
			messages.success(request, "Section d'age a été bien ajouté")
			context['section_age'] = SectionAge.objects.all().values().order_by("created_at").reverse()
		else:
			print("form is not valid")
			messages.error(request,form_validation_error(form))
	return render(request, 'section-age.html', context)

@login_required(login_url="/login/")
def formulaire_modifier_section_age  (request):
	context = {}
	
	if request.method == 'POST':
		id_section_age = request.POST.get("id")
		section_age = SectionAge.objects.get(id = id_section_age)
		context['section_age'] = section_age
		
	return render(request, 'modifier-section-age.html', context)

@login_required(login_url="/login/")	
def update_section_age(request):
	context = {}
	if request.method == 'POST':
		section_age1 = request.POST.get("section_age1")
		section_age2 = request.POST.get("section_age2")
		id_section_age = request.POST.get("id")
		try:
			
			SectionAge.objects.filter(id =id_section_age).update(section_age1=section_age1)
			SectionAge.objects.filter(id =id_section_age).update(section_age2=section_age2)

			
			 
		except Exception as e:
			print(e)
			messages.error(request,'Erreur de modification de section d age')
			context['list_section_age'] = SectionAge.objects.all().values().order_by("created_at").reverse()
			return render(request, 'section-age.html', context)
		
		
		messages.info(request, 'Section d age a été bien modifié')

	context['list_section_age'] = SectionAge.objects.all().values().order_by("created_at").reverse()
	return render(request, 'section-age.html', context)
@login_required(login_url="/login/")
def delete_section_age(request):
	context = {}
	if request.method == 'POST':
		id_section_age = request.POST.get("id")
		section = SectionAge.objects.get(id = id_section_age)
		section.delete()
	messages.info(request, 'Section d age bien supprimé')
	context['list_section_age'] = SectionAge.objects.all().values().order_by("created_at").reverse()
	return render(request, 'section-age.html', context)







