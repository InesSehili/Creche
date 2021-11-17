from django.shortcuts import render, redirect
from django.contrib import messages
from depenses.models import Depense
from depenses.forms import DepenseForm, form_validation_error
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from enfants.models import Enfant
from employes.models import Employes
from pointages.models import Pointage
from besoin.models import Besoin
from factures.models import Facture
from prixsortie.models import Prixsortie
import datetime as dt
from factureenfants.models import FactureEnfant


# Create your views here.

@login_required(login_url="/login/")
def depense_page(request):
	context = {}

	context['list_depense'] = Depense.objects.all().values().order_by("created_at").reverse()
	if request.method =='POST':

		form = DepenseForm(request.POST, request.FILES)
		description = request.POST.get('description')
		print("*****************",description," ***************")
		if form.is_valid():
			print("form is valid")
			form.save()
			messages.success(request, 'Depense a été bien ajouté')
			context['depense'] = Depense.objects.all().values().order_by("created_at").reverse()
		else:
			print("form is not valid")
			messages.error(request,form_validation_error(form))
	return render(request, 'depense.html', context)

@login_required(login_url="/login/")
def formulaire_modifier_depense(request):
	context = {}
	
	if request.method == 'POST':
		id_depense = request.POST.get("id")
		depense = Depense.objects.get(id = id_depense)
		context['depense'] = depense
		
	return render(request, 'modifier-depense.html', context)

@login_required(login_url="/login/")	
def update_depense(request):
	context = {}
	if request.method == 'POST':
		id_depense = request.POST.get("id")
		nom = request.POST.get("nom")
		description = request.POST.get('description')
		try:
			{Depense.objects.filter(id =id_depense).update(nom=nom)}
		except Exception as e:
			print(e)

			messages.error(request,'Dépense existe déja')
			context['list_depense'] = Depense.objects.all().values().order_by("created_at").reverse()
			return render(request, 'depense.html', context)
		
		
		Depense.objects.filter(id = id_depense).update(description=description)
		messages.info(request, 'Depense a été bien modifie')

	context['list_depense'] = Depense.objects.all().values().order_by("created_at").reverse()
	return render(request, 'depense.html', context)
@login_required(login_url="/login/")
def delete_depense(request):
	context = {}
	if request.method == 'POST':
		id_depense = request.POST.get("id")
		try:
			depense = Depense.objects.get(id = id_depense)
			depense.delete()
		except Exception as e:
			print("")

		
	messages.info(request, 'Depense a été bien supprimé')
	context['list_depense'] = Depense.objects.all().values().order_by("created_at").reverse()
	return render(request, 'depense.html', context)



@login_required(login_url="/login/")
def dashboard(request):
	context = {}
	list_employe_alerte_salaire_diff3 = []
	list_employe_alerte_salaire_diff2 = []
	list_employe_alerte_salaire_diff1 = []
	list_employe_alerte_salaire_diff = []
	list_employe_alerte_salaire_diff31 = []
	list_enfant_alerte_paiement_diff3 = []
	list_enfant_alerte_paiement_diff2 = []
	list_enfant_alerte_paiement_diff1 = []
	list_enfant_alerte_paiement_diff = []
	list_enfant_alerte_paiement_diff31 = []
	list_id_employe = []
	list_id_enfant = []
	list_employe = []
	list_enfant_e = []
	revenu_entre = 0
	depense_entre = 0
	reste_total_enfant = 0
	revenu_total = 0
	depense_total = 0
	list_payement = FactureEnfant.objects.all()
	list_depense = Prixsortie.objects.all()
	if request.method=="POST":
		voir= request.POST.get("voir")
		if voir =="revenue":
			date_debut_str = request.POST.get('date_debut')
			print("date de debut",date_debut_str )
			date_fin_str = request.POST.get('date_fin')
			print(" date_fin", date_fin_str)
			date_debut = dt.datetime.strptime(date_debut_str, '%Y-%m-%d')
			date_fin = dt.datetime.strptime(date_fin_str, '%Y-%m-%d')
			print("date_debut", date_debut)
			print("date_fin", date_fin)
			if date_debut > date_fin:
				messages.error(request, "Date de debut ou de fin erroné")
			else :
				list_payement_entre = FactureEnfant.objects.filter(created_at__date__range=[date_debut, date_fin])
				if list_payement_entre.count() !=0:
					for payement in list_payement_entre:
						revenu_entre = revenu_entre + payement.prix_paye
				context['revenu_entre'] = revenu_entre
				print('revenu_entre',revenu_entre )
				context['date_debut'] = date_debut_str 
				context['date_fin'] = date_fin_str
		if voir =="depense":
			date_debut_str_depense = request.POST.get('date_debut_depense')
			print("date de debut_depense",date_debut_str_depense )
			date_fin_str_depense = request.POST.get('date_fin_depense')
			print(" date_fin_depense", date_fin_str_depense)
			date_debut_depense = dt.datetime.strptime(date_debut_str_depense, '%Y-%m-%d')
			date_fin_depense = dt.datetime.strptime(date_fin_str_depense, '%Y-%m-%d')
			print("date_debut_depense", date_debut_depense)
			print("date_fin_depense", date_fin_depense)
			if date_debut_depense > date_fin_depense:
				messages.error(request, "Date de debut ou de fin erroné")

			else :
				list_depense_entre = Prixsortie.objects.filter(created_at__date__range=[date_debut_depense, date_fin_depense])
				if list_depense_entre.count() !=0:
					for depense in list_depense_entre:
						depense_entre = depense_entre + depense.prix_sortie
				context['depense_entre'] = depense_entre
				print('depense_entre',depense_entre )
				context['date_debut_depense'] = date_debut_str_depense 
				context['date_fin_depense'] = date_fin_str_depense
	date_debut = datetime.now(timezone.utc)
	context['segment'] = 'dashboard'
	list_enfant = Enfant.objects.all()

	context['list_enfant'] = list_enfant.count()
	if list_enfant.count() != 0:
		context['date_du_dernier_enfant_ajouter'] = Enfant.objects.last().created_at
		for enf in list_enfant:
			reste_total_enfant = reste_total_enfant + enf.reste_paye

	date_debut_a = datetime.today()
	date_jdida = date_debut_a.date()
	list_pointage_employe = Pointage.objects.filter(raison_pointage='employe').filter(date_pointage = date_jdida )
	list_employe_tout = Employes.objects.all().order_by('updated_at')
	for p in list_pointage_employe:
		list_id_employe.append(p.employe.id)

	context['nbr_absent_employe'] = Employes.objects.exclude(id__in=list_id_employe).count()
	list_pointage_enfant = Pointage.objects.filter(raison_pointage='enfant').filter(date_pointage = date_jdida )
	for p in list_pointage_enfant:
		list_id_enfant.append(p.enfant.id)

	context['nbr_absent_enfant'] = Enfant.objects.exclude(id__in=list_id_enfant).count()

	for p in list_pointage_employe:
		list_employe.append(Employes.objects.get(id = p.employe.id))

	context['nbr_presnet_employe'] =len(list_employe)
	for p in list_pointage_enfant:
		list_enfant_e.append(Enfant.objects.get(id = p.enfant.id))

	context['nbr_presnet_enfant'] =len(list_enfant_e)
	employes = Employes.objects.all()
	for emp in employes:
		diff = abs(((date_debut-emp.created_at)).days)
		print("diff", diff)
		if diff >= 3:
			diff_3 = abs((date_debut-emp.created_at).days)+3
			diff_2 = abs((date_debut-emp.created_at).days)+2
			diff_1 = abs((date_debut-emp.created_at).days)+1
			diff_31 = abs((date_debut-emp.created_at).days)-1
			print("Sama7 ",diff_31)
			if diff_3 % 30 == 0:
				list_employe_alerte_salaire_diff3.append(emp)
			if diff_2 % 30 == 0:
				list_employe_alerte_salaire_diff2.append(emp)
			if diff_1 % 30 == 0:
				list_employe_alerte_salaire_diff1.append(emp)
			if diff % 30 == 0:
				list_employe_alerte_salaire_diff.append(emp)
			if diff_31 % 30 == 0:
				list_employe_alerte_salaire_diff31.append(emp)


	context['list_employe_alerte_salaire_diff3'] = list_employe_alerte_salaire_diff3
	context['list_employe_alerte_salaire_diff2'] = list_employe_alerte_salaire_diff2
	context['list_employe_alerte_salaire_diff1'] = list_employe_alerte_salaire_diff1
	context['list_employe_alerte_salaire_diff'] = list_employe_alerte_salaire_diff
	context['list_employe_alerte_salaire_diff31'] = list_employe_alerte_salaire_diff31

	enfants = Enfant.objects.all()
	for enf in enfants:
		diff = abs(((date_debut-enf.created_at)).days)
		print("diff", diff)
		if diff >= 3:
			diff_3 = abs((date_debut-enf.created_at).days)+3
			diff_2 = abs((date_debut-enf.created_at).days)+2
			diff_1 = abs((date_debut-enf.created_at).days)+1
			diff_31 = abs((date_debut-enf.created_at).days)-1
			print("Sama7 ",diff_31)
			if diff_3 % 30 == 0:
				list_enfant_alerte_paiement_diff3.append(enf)
			if diff_2 % 30 == 0:
				list_enfant_alerte_paiement_diff2.append(enf)
			if diff_1 % 30 == 0:
				list_enfant_alerte_paiement_diff1.append(enf)
			if diff % 30 == 0:
				list_enfant_alerte_paiement_diff.append(enf)
			if diff_31 % 30 == 0:
				list_enfant_alerte_paiement_diff31.append(enf)
	

	context['list_enfant_alerte_paiement_diff3'] = list_enfant_alerte_paiement_diff3
	context['list_enfant_alerte_paiement_diff2'] = list_enfant_alerte_paiement_diff2
	context['list_enfant_alerte_paiement_diff1'] = list_enfant_alerte_paiement_diff1
	context['list_enfant_alerte_paiement_diff'] = list_enfant_alerte_paiement_diff
	context['list_enfant_alerte_paiement_diff31'] = list_enfant_alerte_paiement_diff31

	print('enfz', list_enfant_alerte_paiement_diff1)
	print('enfz', list_enfant_alerte_paiement_diff31)
	print('enfz', list_enfant_alerte_paiement_diff)
	print('enfz', list_enfant_alerte_paiement_diff2)
	print('enfz', list_enfant_alerte_paiement_diff3)
	context['reste_total_enfant'] = reste_total_enfant

	context['list_besoins'] = Besoin.objects.all().order_by('updated_at')[:5]
	if list_payement.count() !=0:
		for payement in list_payement:
			revenu_total = revenu_total+ payement.prix_paye

	if list_depense.count() !=0:
		for depense in list_depense:
			depense_total = depense_total+ depense.prix_sortie

	context['revenu_total'] = revenu_total
	context['depense_total'] = depense_total






















	return render(request, 'dashboard.html', context)


	







 		



 
    	











    
    
    
    
















