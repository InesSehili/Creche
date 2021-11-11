from django.shortcuts import render , redirect
from employes.forms import EmployeeForm, form_validation_error
from django.contrib import messages
from employes.models import Employes
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileWriter, PdfFileReader
from creches.models import Creche
import datetime
from factures.models import Facture

# Create your views here.
@login_required(login_url="/login/")
def ajouter_employee(request):
    context = {}
    context['segment'] = 'employe'
    if request.method == "POST":
        form = EmployeeForm(request.POST or None)
        if form.is_valid():
            print("is valid")
            form.save()
            messages.success(request, 'Employee a été bien ajouté')
        else:
            print("is not valid")
            print(form_validation_error(form))
            messages.error(request, "Numero de telephone doit etre unique")
    
    context['list_employee'] = Employes.objects.all().values()
    return render(request, 'ajouter-employee.html', context)


@login_required(login_url="/login/")
def liste_employe(request):
    context = {}
    context['segment'] = 'employe'
    context['list_employee'] = Employes.objects.all().values().order_by('updated_at')
    return render(request, 'employes.html', context)

@login_required(login_url="/login/")
def supprimer_employe(request):
    context = {}
    context['segment'] = 'employe'
    if request.method =="POST":
        employe = request.POST.get("employe")
        print("employe = ", employe)
        Employes.objects.get(id=employe).delete()
    
    
    
    return redirect('liste_employe')
@login_required(login_url="/login/")
def modifier_employe(request):
    context = {}
    context['segment'] = 'employe'
    if request.method =="POST":
        idemploye = request.POST.get("id")
        employe = Employes.objects.get(id=idemploye)
    
    context ['employe'] = employe
    return render(request, 'modifier-employe.html', context)

@login_required(login_url="/login/")
def update_employee(request):
    context = {}
    if request.method == 'POST':
        id_employe = request.POST.get("id")
        nom = request.POST.get("nom")
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        address = request.POST.get('address')
        fonction=request.POST.get('fonction')
        email = request.POST.get('email')
        salaire = request.POST.get('salaire')

        Employes.objects.filter(id = id_employe).update(nom=nom)
        Employes.objects.filter(id = id_employe).update(prenom=prenom)
        Employes.objects.filter(id = id_employe).update(telephone=telephone)
        Employes.objects.filter(id = id_employe).update(address=address)
        Employes.objects.filter(id = id_employe).update(email=email)
        Employes.objects.filter(id = id_employe).update(salaire=salaire)
        Employes.objects.filter(id = id_employe).update(fonction=fonction)
        messages.info(request, 'Employe a été bien modifie')
    
    
    return redirect('liste_employe')

@login_required(login_url="/login/")
def employe_list_pointage(request):
    context = {}
    if request.method =="POST":
        id_employe = request.POST.get("employe")

    p = Employes.objects.get(id = id_employe)
    pointage = Pointage.objects.filter(employe=p)
    return render(request, 'employes.html', context)

@login_required(login_url="/login/")
def imprimer_facture_employer(request):

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",12)
    if request.method =="POST":
        id_facture_enfant = request.POST.get('facture')
        id_employe = request.POST.get('employe')
        date_facture = request.POST.get('date')
     

    facture_objet = Facture.objects.get(id = id_facture_enfant)
    creche = Creche.objects.get(id = Creche.objects.last().id)
    
    
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
    employe = facture_objet.employe.nom + ''+ facture_objet.employe.prenom


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
    

    c.drawString(320, 317, "Employe: " + employe)

    c.drawString(320, 347, "Telephone: " + facture_objet.employe.telephone)
    c.drawString(320, 364, "Adresse: " + facture_objet.employe.address)

    c.drawString(475, 223, date_sur_facture)
    c.drawString(475, 258,str(num_facture))
    c.drawString(78, 424, "Salaire: ")
    c.drawString(465, 424, str(facture_objet.tarif))
    c.drawString(465,608 ,str(facture_objet.tarif))


    total_facture = facture_objet.tarif
    c.drawString(465,580,str(total_facture))
    c.showPage()
    c.save()
    buf.seek(0)
    new_pdf = PdfFileReader(buf)
    output = PdfFileWriter()
    existing_pdf = PdfFileReader(open("creche-model-facture-employe.pdf", "rb"))
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    outputStream = open("destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    return FileResponse(open("destination.pdf", 'rb'), content_type='application/pdf')   





