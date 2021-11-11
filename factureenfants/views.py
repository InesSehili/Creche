from django.shortcuts import redirect, render
from factureenfants.models import FactureEnfant
from enfants.models import Enfant
from categoriesAbonnement.models import CategorieAbonnement
from supplement.models import Supplement
from django.contrib import messages
from  payement.models import Payement
import decimal
from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileWriter, PdfFileReader
from creches.models import Creche
import datetime
from django.contrib.auth.decorators import login_required
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from django.http import HttpResponse
cm = 2.54

# Create your views here.
@login_required(login_url="/login/")
def add_new_facture_enfant(request):
	context ={}
	if request.method =="POST" :
		id_enfant = request.POST.get('enfant')
		categorie = request.POST.get("categorie")
		suplement = request.POST.getlist("suplement[]")
		suplement_autre = request.POST.getlist("suplement-autre[]")
		client = request.POST.get("client")
		print("client",client)
		frais_inscription =decimal.Decimal( request.POST.get("frais_inscription"))
		prix_paye = decimal.Decimal(request.POST.get("prix_paye"))
	prix_categorie = 0
	prix_supplement = 0
	if categorie :
		categorieAbonnement = CategorieAbonnement.objects.get(id = categorie)
		prix_categorie = categorieAbonnement.prix
	if suplement :
		for i in range(len(suplement)):
			obj_supplement = Supplement.objects.get(id=suplement[i])
			prix_supplement = prix_supplement + obj_supplement.prix
	if suplement_autre :
		for i in range(len(suplement_autre)):
			obj_supplement = Supplement.objects.get(id=suplement_autre[i])
			prix_supplement = prix_supplement + obj_supplement.prix
	total_payement = frais_inscription + prix_categorie + prix_supplement 
	rest_paye =  total_payement - prix_paye
	print('prix_paye', prix_paye)
	print('total_payement',total_payement)
	print('rest_paye', rest_paye)
	if prix_paye <= total_payement :
		enfant = Enfant.objects.get(id =id_enfant)
		total_payement_auj = frais_inscription + prix_categorie + prix_supplement
		total_payement_pre = enfant.total_payement 
		total_payement_enfant = total_payement_auj + total_payement_pre
		prix_paye_pre = enfant.prix_paye
		total_prix_paye = prix_paye_pre+ prix_paye
		rest_paye_enfant = total_payement_enfant - total_prix_paye
		print("total_prix_paye",total_prix_paye )
		print("total_payement_enfant",total_payement_enfant )
		print("reste enfant",rest_paye_enfant )
		Enfant.objects.filter(id = id_enfant).update(prix_paye = total_prix_paye)
		Enfant.objects.filter(id = id_enfant).update(reste_paye = rest_paye_enfant)
		Enfant.objects.filter(id = id_enfant).update(total_payement = total_payement_enfant)
		facture_enfant = FactureEnfant(enfant=enfant,categorie=categorieAbonnement,client = client, frais_inscription=frais_inscription, prix_paye =prix_paye , reste_paye = rest_paye , prix_total = total_payement )
		facture_enfant.save()

		payement_enfant = Payement(enfant = enfant , facture = facture_enfant , prix_payer = prix_paye , client = client, reste_facture_apres_ce_paiment = rest_paye)
		payement_enfant.save()

		if suplement_autre :
			for i in range(len(suplement_autre)):
				obj_supplement = Supplement.objects.get(id=suplement_autre[i])
				if(True):
					facture_enfant.supplement.add((obj_supplement))	
		if suplement :
			for i in range(len(suplement)):
				obj_supplement = Supplement.objects.get(id=suplement[i])
				if(True):
					facture_enfant.supplement.add((obj_supplement))	
		 		
		messages.success(request, "Facture de l'enfant a été bien ajouter")
	else:
		messages.error(request,"Le prix payé est superieur du reste")
		redirect('formulaire_ajouter_facture')
	context['enfant'] = enfant
	context['list_factures'] = FactureEnfant.objects.filter(enfant=enfant).order_by('updated_at')
	return render(request, 'facture-enfant.html',context) 

@login_required(login_url="/login/")
def liste_factures_enfant(request):
    context={}
    context['segment'] = 'enfant'
    if request.method =="POST": 
        id_enfant = request.POST.get('enfant')


    enfant = Enfant.objects.get(id=id_enfant)
    context['enfant'] = enfant
    context['list_factures'] = FactureEnfant.objects.filter(enfant=enfant).order_by('updated_at')
    return render(request, 'facture-enfant.html',context)
@login_required(login_url="/login/")
def liste_factures_touts_les_enfant(request):
    context={}
    context['segment'] = ''

    context['list_factures'] = FactureEnfant.objects.all().order_by('updated_at')
    return render(request, 'facture-tous-enfant.html',context)

@login_required(login_url="/login/")
def formulaire_ajouter_facture(request):
	context = {}
	list_supplement_autre = []
	context['segment'] = 'enfant'
	if request.method =="POST":
		id_enfant = request.POST.get('enfant')
	enfant = Enfant.objects.get(id=id_enfant)
	facture = FactureEnfant.objects.filter(enfant=enfant).last()
	if facture:
		list_suplement = facture.supplement.all()
		context['list_supplement'] =list_suplement
		for supp in list_suplement:
			list_supplement_autre.append(supp.id)

	
	
		
	context['list_supplement_autre'] = Supplement.objects.exclude(id__in=list_supplement_autre)
	context['list_categories'] =CategorieAbonnement.objects.all().order_by('updated_at')

	context['enfant'] = enfant
	context['facture'] = facture
	return render(request, 'ajouter-facture-enfant.html',context)



@login_required(login_url="/login/")
def update_facture_enfant(request):
	context ={}
	if request.method =="POST" :
		id_enfant = request.POST.get('enfant')
		id_facture = request.POST.get('facture')
		print("id facture = ",id_facture)
		categorie = request.POST.get("categorie")
		suplement = request.POST.getlist("suplement[]")
		suplement_autre = request.POST.getlist("suplement-autre[]")
		client = request.POST.get("client")
		print("client",client)
		frais_inscription =decimal.Decimal( request.POST.get("frais_inscription"))
	prix_categorie = 0
	prix_supplement = 0
	if categorie :
		categorieAbonnement = CategorieAbonnement.objects.get(id = categorie)
		prix_categorie = categorieAbonnement.prix
		if suplement :
			for i in range(len(suplement)):
				obj_supplement = Supplement.objects.get(id=suplement[i])
				prix_supplement = prix_supplement + obj_supplement.prix
		if suplement_autre :
			for i in range(len(suplement_autre)):
				obj_supplement = Supplement.objects.get(id=suplement_autre[i])
				prix_supplement = prix_supplement + obj_supplement.prix
		total_payement = frais_inscription + prix_categorie + prix_supplement
		facture = FactureEnfant.objects.get(id =id_facture)
		prix_paye = facture.prix_paye
		rest_paye =  total_payement - prix_paye
		enfant = Enfant.objects.get(id =id_enfant)
		total_payement_auj = frais_inscription + prix_categorie + prix_supplement
		total_payement_pre = enfant.total_payement
		total_payement_enfant = total_payement_auj + total_payement_pre
		prix_paye_pre = enfant.prix_paye
		 
		total_prix_paye = prix_paye_pre+ prix_paye
		rest_paye_enfant = total_payement_enfant - total_prix_paye
		Enfant.objects.filter(id = id_enfant).update(prix_paye = total_prix_paye)
		Enfant.objects.filter(id = id_enfant).update(reste_paye = rest_paye_enfant)
		Enfant.objects.filter(id = id_enfant).update(total_payement = total_payement_enfant)
		FactureEnfant.objects.filter(id = id_facture).update(categorie=categorieAbonnement)
		FactureEnfant.objects.filter(id = id_facture).update(client = client)
		FactureEnfant.objects.filter(id = id_facture).update(frais_inscription=frais_inscription)
		FactureEnfant.objects.filter(id = id_facture).update(reste_paye = rest_paye)
		FactureEnfant.objects.filter(id = id_facture).update(prix_total = total_payement)
		facture.supplement.clear()
		if suplement_autre :
			for i in range(len(suplement_autre)):
				obj_supplement = Supplement.objects.get(id=suplement_autre[i])
				if(True):
					facture.supplement.add((obj_supplement))
		print("suplement",suplement)
		if suplement :
			for i in range(len(suplement)):
				obj_supplement = Supplement.objects.get(id=suplement[i])
				if(True):
					facture.supplement.add((obj_supplement))
		messages.warning(request, "Facture a été bien modifiée")
		context['enfant'] = enfant
		context['list_factures'] = FactureEnfant.objects.filter(enfant=enfant).order_by('updated_at')
		return render(request, 'facture-enfant.html',context)





@login_required(login_url="/login/")
def formulaire_modifier_facture_enfant(request):
	context ={}
	list_supplement_autre = []
	context['segment'] = 'enfant'
	if request.method =="POST":
		id_enfant = request.POST.get('enfant')
		id_facture = request.POST.get('facture')
	enfant = Enfant.objects.get(id=id_enfant)
	facture = FactureEnfant.objects.get(id=id_facture)
	print("facture",facture)

	if facture:
		try:
			list_suplement = facture.supplement.all()
			context['list_supplement'] =list_suplement
			for supp in list_suplement:
				list_supplement_autre.append(supp.id)
		except Exception as e:
			print(e)
		
		
		
			

	print("longuer ",len(list_supplement_autre))
	
	if len(list_supplement_autre) == 0 :
		context['list_supplement_autre'] = Supplement.objects.all()
	else :
		context['list_supplement_autre'] = Supplement.objects.exclude(id__in=list_supplement_autre)

	
	context['list_categories'] =CategorieAbonnement.objects.all().order_by('updated_at')

	context['enfant'] = enfant
	context['facture'] = facture
	return render(request, 'modifier-facture-enfant.html',context)






	

@login_required(login_url="/login/")
def delete_facture(request):
	context={}
	context['segment'] = 'enfant'
	if request.method =="POST":
		id_enfant = request.POST.get('enfant')
		id_facture = request.POST.get('facture')

	enfant = Enfant.objects.get(id=id_enfant)
	facture = FactureEnfant.objects.get(id=id_facture)
	prix_paye_facture =facture.prix_paye
	reste_paye_facture = facture.reste_paye
	prix_total_facture = facture.prix_total
	total_payement_enfant = enfant.total_payement
	prix_paye_enfant = enfant.prix_paye 
	
	Enfant.objects.filter(id = id_enfant).update(prix_paye = prix_paye_enfant-prix_paye_facture )
	Enfant.objects.filter(id = id_enfant).update(total_payement = total_payement_enfant-prix_total_facture )
	enfant = Enfant.objects.get(id=id_enfant)
	nv_reste = enfant.total_payement-enfant.prix_paye
	Enfant.objects.filter(id = id_enfant).update(reste_paye = nv_reste )
	facture.delete()
	context['list_factures'] = FactureEnfant.objects.filter(enfant=enfant).order_by('updated_at')
	context['enfant'] = enfant
	messages.info(request,"Suppression a été bien effectué")
	return render(request, 'facture-enfant.html',context)



@login_required(login_url="/login/")
def imprimer_facture(request):
	buf = io.BytesIO()
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica",12)
	if request.method =="POST":
		id_facture_enfant = request.POST.get('facture')
		id_enfant = request.POST.get('enfant')
		date_facture = request.POST.get('date')
		id_paiement = request.POST.get('payement')

	facture_objet = FactureEnfant.objects.get(id = id_facture_enfant)
	creche = Creche.objects.get(id = Creche.objects.last().id)
	paiement = Payement.objects.get(id = id_paiement)
	
	sample_str = date_facture.split()[0]
	month_name = sample_str[0:3]
	print(month_name)
	datetime_object = datetime.datetime.strptime(month_name, "%b")
	month_number = datetime_object.month
	day_number = date_facture.split()[1]
	year_number = date_facture.split()[2]
	date_sur_facture = day_number[:-1]+"/"+ str(month_number)+"/"+ year_number[:-1]
	
	nom_creche = creche.nom
	adresse_creche = creche.adresse
	num1_creche = creche.telephone1
	if creche.telephone2:
		num2_creche = creche.telephone2

	rc = creche.rc
	num_facture = facture_objet.id
	gerant = creche.gerant
	parent = facture_objet.client
	tel_parent = ""
	print("client = ", parent)

	if facture_objet.client == 'mere':
		parent = facture_objet.enfant.parents.mere
		tel_parent = facture_objet.enfant.parents.telephone_mere
	if facture_objet.client == 'pere':
		parent = facture_objet.enfant.parents.pere
		tel_parent = facture_objet.enfant.parents.telephone_pere
	c.drawString(78, 150, nom_creche)
	c.drawString(78, 170, adresse_creche)
	c.drawString(78, 190, "Téléphone:")
	c.drawString(150, 190, num1_creche)

	if creche.telephone2:
		c.drawString(218, 190, "/")
		c.drawString(222, 190, num2_creche )

	c.drawString(78, 210, 'Rc: ')
	c.drawString(98, 210, rc)

	c.drawString(78, 317, gerant)
	c.drawString(78, 334, "Téléphone:"+num1_creche)
	if creche.telephone2:
		c.drawString(205, 334, "/")
		c.drawString(209, 334, num2_creche )
	

	c.drawString(320, 317, "Parent: " + parent)
	c.drawString(320, 330, "Enfant: " + facture_objet.enfant.nom +" "+ facture_objet.enfant.prenom)
	c.drawString(320, 347, "Telephone: " + tel_parent)
	c.drawString(320, 364, "Adresse: " + facture_objet.enfant.parents.adresse)

	c.drawString(475, 223, date_sur_facture)
	c.drawString(475, 258,str(num_facture))
	categorie  = facture_objet.categorie.nom
	categorie_prix  = facture_objet.categorie.prix
	c.drawString(78, 424, "Categorie abonnement: "+categorie)
	c.drawString(465, 424, str(categorie_prix))
	frais_inscription = facture_objet.frais_inscription
	c.drawString(78, 444, "Frais d'inscription")
	c.drawString(465, 444, str(frais_inscription))
	supplement = facture_objet.supplement.all()
	x_supplement = 78
	y_supplement = 464
	x_supplement_prix = 465
	y_supplement_prix = 464
	for sup in supplement:
		c.drawString(x_supplement, y_supplement, "Supplement: "+sup.nom_supplement)
		y_supplement = y_supplement+20
		c.drawString(x_supplement_prix, y_supplement_prix, str(sup.prix))
		y_supplement_prix = y_supplement_prix+20



	total_facture = facture_objet.prix_total
	c.drawString(465,580,str(total_facture))
	reste_avant_paiement = facture_objet.reste_paye
	prix_payer = paiement.prix_payer
	c.drawString(465,608 ,str(prix_payer))
	reste_payer = paiement.reste_facture_apres_ce_paiment
	c.drawString(465,635,str(reste_payer))
	c.showPage()
	c.save()
	buf.seek(0)
	new_pdf = PdfFileReader(buf)
	output = PdfFileWriter()
	existing_pdf = PdfFileReader(open("creche-model-facture.pdf", "rb"))
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)
	outputStream = open("destination.pdf", "wb")
	output.write(outputStream)
	outputStream.close()
	return FileResponse(open("destination.pdf", 'rb'), content_type='application/pdf')




def print_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Tableau.pdf'

    elements = []

    doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=6.5 * cm, topMargin=0.3 * cm, bottomMargin=0)

    data=[(1,2),(3,4)]
    table = Table(data, colWidths=270, rowHeights=79)
    elements.append(table)
    doc.build(elements) 
    return response




















