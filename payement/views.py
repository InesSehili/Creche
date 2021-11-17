from django.shortcuts import render , redirect
from factureenfants.models import FactureEnfant 
from payement.models import Payement
import decimal
from django.contrib.auth.decorators import login_required
from payement.forms import PaymentForm , form_validation_error
from django.contrib import messages
from enfants.models import Enfant


# Create your views here.
@login_required(login_url="/login/")
def formulaire_creation_payement(request):
	context = {}
	if request.method =="POST":
		id_enfant = request.POST.get('id')
		nom_enfant = request.POST.get('nom')
		prenom_enfant = request.POST.get('prenom')
        # context['liste_consultation_non_payees'] =  Consultation.objects.exclude(reste=0).filter(patient =id_patient)
		context['nom'] = nom_enfant
		context['prenom'] = prenom_enfant
		context['enfant'] = id_enfant
	
		context['liste_facture_non_payees'] = FactureEnfant.objects.exclude(reste_paye=0).filter(enfant=id_enfant)
		liste_payment = Payement.objects.filter(enfant = id_enfant )
		context['list_payement'] = liste_payment

	
	return render(request, "payment-enfant.html", context)

@login_required(login_url="/login/")
def ajouter_payement(request):
	
	context = {}
	context['list_Enfants'] = Enfant.objects.all().order_by('updated_at')
	if request.method =="POST":
		id_enfant = request.POST.get('enfant')
		prix_payer = decimal.Decimal(request.POST.get('prix_payer'))
		client = request.POST.get('client')
		facture = request.POST.get('facture')

		reste_facture =FactureEnfant.objects.get(id=decimal.Decimal(facture)).reste_paye          
		prix_payer_facture =FactureEnfant.objects.get(id=decimal.Decimal(facture)).prix_paye          
		prix_defini_facture =FactureEnfant.objects.get(id=decimal.Decimal(facture)).prix_total

		

		if prix_payer <= reste_facture : 
			form = PaymentForm(request.POST or None)
			if form.is_valid():
				form.save() 
				FactureEnfant.objects.filter(id=decimal.Decimal(facture)).update(prix_paye= prix_payer_facture+decimal.Decimal(prix_payer))
				dernier_prix_paye = FactureEnfant.objects.get(id=decimal.Decimal(facture)).prix_paye
				FactureEnfant.objects.filter(id=decimal.Decimal(facture)).update(reste_paye= prix_defini_facture-dernier_prix_paye)
				last_paiement = Payement.objects.last().id
				Payement.objects.filter(id = last_paiement).update(reste_facture_apres_ce_paiment = prix_defini_facture-dernier_prix_paye)
				prix_paye_patient = Enfant.objects.get(id=id_enfant).prix_paye
				Enfant.objects.filter(id=id_enfant).update(prix_paye=prix_paye_patient+ decimal.Decimal(prix_payer) )
				prix_paye_patient_2 = Enfant.objects.get(id=id_enfant).prix_paye

				prix_total_patient = Enfant.objects.get(id=id_enfant).total_payement
				Enfant.objects.filter(id=id_enfant).update(reste_paye=prix_total_patient- prix_paye_patient_2)
				messages.info(request, "payements a été bien enregistré")
				
			else :
				messages.error(request, "prix paye de facture est superieur du reste de payements")
				nom_enfant =request.POST.get('nom')
				prenom_enfant =request.POST.get('prenom')

				context['nom'] = nom_enfant
				context['prenom'] = prenom_enfant
				context['enfant'] = id_enfant
		
				context['liste_facture_non_payees'] = FactureEnfant.objects.exclude(reste_paye=0).filter(enfant=id_enfant)
				liste_payment = Payement.objects.filter(enfant = id_enfant )
				context['list_payement'] = liste_payment
				context ['facture_sel'] =  facture
				messages.error(request, "le prix doit etre superieur ou egal a 0")
				return render(request, "payment-enfant.html", context) 
				
		else:
			
			messages.error(request, "prix paye de facture est superieur du reste de payements")
			nom_enfant =request.POST.get('nom')
			prenom_enfant =request.POST.get('prenom')
			context['nom'] = nom_enfant
			context['prenom'] = prenom_enfant
			context['enfant'] = id_enfant
	
			context['liste_facture_non_payees'] = FactureEnfant.objects.exclude(reste_paye=0).filter(enfant=id_enfant)
			liste_payment = Payement.objects.filter(enfant = id_enfant )
			context['list_payement'] = liste_payment
			context ['facture_sel'] =  facture 
			return render(request, "payment-enfant.html", context)  

	
	return render(request, "liste-enfants.html", context )
@login_required(login_url="/login/")   
def supprimer_payement(request):
	
	context = {}
	context['list_Enfants'] = Enfant.objects.all().order_by('updated_at')
	if request.method =="POST":
		payement = request.POST.get("id_payement")
		# prix_payer = request.POST.get("prix_payer")
		
		payement_obj = Payement.objects.get(id =payement)
		prix_payer = payement_obj.prix_payer
		facture = Payement.objects.get(id =payement).facture
		id_facture =facture.id
		print ("facture " , id_facture)  
		id_enfant = payement_obj.enfant.id
		reste_facture_prec =FactureEnfant.objects.get(id=id_facture).reste_paye
		prix_payer_facture_prec =FactureEnfant.objects.get(id=id_facture).prix_paye
		
		FactureEnfant.objects.filter(id=id_facture).update(prix_paye= prix_payer_facture_prec - prix_payer)
		FactureEnfant.objects.filter(id=id_facture).update(reste_paye= reste_facture_prec +prix_payer)


		prix_paye_patient_prec = Enfant.objects.get(id=id_enfant).prix_paye
		Enfant.objects.filter(id=id_enfant).update(prix_paye=prix_paye_patient_prec -prix_payer )
		

		reste_paye_enfant_prec = Enfant.objects.get(id=id_enfant).reste_paye
		Enfant.objects.filter(id=id_enfant).update(reste_paye=reste_paye_enfant_prec +  prix_payer)
		Payement.objects.get(id=payement).delete()
		messages.info(request, 'payement enfant a ete bien supprimer ')
	
	return render(request, "liste-enfants.html", context )
@login_required(login_url="/login/")
def modifier_payement(request):

	context = {}
	if request.method =="POST":

		context['nom'] = request.POST.get('nom')
		context['prenom'] = request.POST.get('prenom')
		context['enfant'] = request.POST.get('id')

		id_payement = request.POST.get("id_payement")
		payement = Payement.objects.get(id=id_payement)
		context['payement'] =payement
		
	return  render(request, 'modifier-payements-enfant.html',context)
@login_required(login_url="/login/")  
def valider_modifier_payement(request):
	
	context = {}
	if request.method =="POST":
		id_payement = request.POST.get("id_payement")
		prix_payer = decimal.Decimal(request.POST.get('prix_payer'))
		client = request.POST.get('client')
		id_enfant = request.POST.get('enfant')
		facture = request.POST.get('facture')

		print("******facture " , facture)
		payement = Payement.objects.get(id=id_payement)
		context['payement'] =payement
		reste_facture =FactureEnfant.objects.get(id=facture).reste_paye          
		prix_payer_facture =FactureEnfant.objects.get(id=facture).prix_paye          
		prix_defini_facture =FactureEnfant.objects.get(id=facture).prix_total
		
		          
		prix_payer_payement =Payement.objects.get(id=id_payement).prix_payer          
		if prix_payer != prix_payer_payement :
			# prix_payer_new = prix_payer_facture - prix_payer_payement
			reste_facture_new = reste_facture - prix_payer_payement + prix_payer

			prix_payer_facture_new = prix_payer_facture - prix_payer_payement + prix_payer 
			reste = reste_facture + prix_payer_payement
			reste_facture_new = prix_defini_facture - prix_payer_facture_new
			print("reste facture ******** " ,  reste_facture_new)
			print("prix_payer_facture_new  ******** " ,  prix_payer_facture_new)

			if prix_payer <= reste : 
					
					Payement.objects.filter(id =decimal.Decimal(id_payement) ).update(prix_payer = prix_payer)
					Payement.objects.filter(id =decimal.Decimal(id_payement) ).update(client = client)

					FactureEnfant.objects.filter(id=decimal.Decimal(facture)).update(prix_paye= prix_payer_facture + decimal.Decimal(prix_payer)- prix_payer_payement )
					dernier_prix_paye = FactureEnfant.objects.get(id=decimal.Decimal(facture)).prix_paye
					FactureEnfant.objects.filter(id=decimal.Decimal(facture)).update(reste_paye= prix_defini_facture-dernier_prix_paye)
					Payement.objects.filter(id =decimal.Decimal(id_payement)).update(reste_facture_apres_ce_paiment = prix_defini_facture-dernier_prix_paye)
					
					prix_paye_patient = Enfant.objects.get(id=id_enfant).prix_paye
					Enfant.objects.filter(id=id_enfant).update(prix_paye=prix_paye_patient+ decimal.Decimal(prix_payer) - prix_payer_payement )
					prix_paye_patient_2 = Enfant.objects.get(id=id_enfant).prix_paye

					prix_total_patient = Enfant.objects.get(id=id_enfant).total_payement
					Enfant.objects.filter(id=id_enfant).update(reste_paye=prix_total_patient- prix_paye_patient_2)
					messages.info(request, "payements a été bien modifie")
						 					
			else:
				
				messages.error(request, "Prix paye est superieur du reste de facture")
				context['nom'] = request.POST.get('nom')
				context['prenom'] = request.POST.get('prenom')
				context['enfant'] = request.POST.get('enfant')

				id_payement = request.POST.get("id_payement")
				payement = Payement.objects.get(id=id_payement)
				context['payement'] =payement
		
				
				
				return  render(request, 'modifier-payements-enfant.html',context)
		else :
			Payement.objects.filter(id =decimal.Decimal(id_payement)).update(client = client)
			messages.info(request, "payements a été bien modifie")
						
	context['nom'] = request.POST.get('nom')
	context['prenom'] = request.POST.get('prenom')
	context['enfant'] = request.POST.get('enfant')
	id_enfant = request.POST.get('enfant')
	
	context['liste_facture_non_payees'] = FactureEnfant.objects.exclude(reste_paye=0).filter(enfant=id_enfant)
	liste_payment = Payement.objects.filter(enfant = id_enfant )
	context['list_payement'] = liste_payment			
	return  render(request, 'payment-enfant.html',context)
  

