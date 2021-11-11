from django.shortcuts import render, redirect
from creches.forms import CrecheForm, form_validation_error
from django.contrib import messages
from creches.models import Creche
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url="/login/")
def ajouter_info_creche(request):
	context = {}
	context['segment'] = 'creche'
	context['creche'] = Creche.objects.last()

	if request.method == 'POST':
		id_creche = request.POST.get('id_creche')
		form = CrecheForm(request.POST, request.FILES)
		if form.is_valid():
			print("form is valid")
			print("id_creche", id_creche)
			if id_creche:
				print('is not None')
				Creche.objects.filter(id = id_creche).update(nom=form.cleaned_data.get('nom') )
				Creche.objects.filter(id = id_creche).update(gerant =form.cleaned_data.get('gerant') )
				Creche.objects.filter(id = id_creche).update(nif =form.cleaned_data.get('nif') )
				Creche.objects.filter(id = id_creche).update(rc =form.cleaned_data.get('rc') )
				Creche.objects.filter(id = id_creche).update(telephone1 =form.cleaned_data.get('telephone1') )
				Creche.objects.filter(id = id_creche).update(telephone2 =form.cleaned_data.get('telephone2') )
				Creche.objects.filter(id = id_creche).update(email =form.cleaned_data.get('email') )
				Creche.objects.filter(id = id_creche).update(adresse =form.cleaned_data.get('adresse') )
				
				messages.success(request, 'Profile saved successfully')
				context['creche'] = Creche.objects.get(id = id_creche)

			else:
				print("is none")
				creche = form.save()
				messages.success(request, 'Profile saved successfully')
				context['creche'] = Creche.objects.get(id = Creche.objects.last().id)
				
				
			   
		else:
			messages.error(request,form_validation_error(form) )
	
    
	return render(request, "creche.html", context)
@login_required(login_url="/login/")
def changer_mot_de_passe(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		print("*******", username)
		u = None
	try:
		u = User.objects.get(username=username)
	except Exception as e:
		messages.error(request, "L'utilisateur ou les mots de passes ne sont pas valide")
		return render(request, 'reset-password.html',{})
	
	if u is not None and password1== password2 :

		try:
			u.set_password(password1)
			u.save()
			messages.success(request, 'Vous avez changez votre mot de passe reconnectez-Vous!')
			redirect('logout')	
		except Exception as e:
			print(e)
			messages.error(request, "Le mot de passe est faible")
			return render(request, 'reset-password.html',{}) 
		
		
		
	else:
		messages.error(request, "L'utilisateur ou les mots de passes ne sont pas valide")
		return render(request, 'reset-password.html',{})

	return render(request, 'reset-password.html',{}) 


	




