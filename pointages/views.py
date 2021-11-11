from django.shortcuts import render ,redirect
from employes.models import Employes
from django.contrib import messages
from pointages.forms import PointageForm ,form_validation_error
import pandas
from pointages.models import Pointage
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.timezone import datetime 
from enfants.models import Enfant
import decimal
from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileWriter, PdfFileReader
from creches.models import Creche
import datetime as dt
from datetime import date, timedelta


# Create your views here.
@login_required(login_url="/login/")
def ajouter_pointage_enfant(request):
    context = {}
    
    context['segment'] = 'poinatge'
    date_debut = datetime.today()

    if request.method =="POST":
        nom = request.POST.get('nom')
        id_enfant = request.POST.get('enfant')
        enfant_objects = Enfant.objects.get(id = id_enfant)
        poitage_enfant = Pointage(enfant=enfant_objects, date_pointage = date_debut, raison_pointage='enfant')
        poitage_enfant.save()
        messages.success(request, "presence de l'enfant a été bien enregistré") 
    else:

        messages.error(request, "Erreur d'indiquer la presence")

   
    
    return redirect('list_enfant_absent')



@login_required(login_url="/login/")
def ajouter_pointage_employe(request):
    context = {}
    
    context['segment'] = 'poinatge'
    date_debut = datetime.today()

    
    if request.method =="POST":
        nom = request.POST.get('nom')
        id_employe = request.POST.get('employe')
        #date_pointage_str = request.POST.get('date_pointage')
        #date_pointage = dt.datetime.strptime(date_pointage_str, '%Y-%m-%dT%H:%M')
        #if date_pointage.day == date_debut.day and date_pointage.month and date_pointage.year:
        employe_objects = Employes.objects.get(id = id_employe)
        poitage_employee = Pointage(employe=employe_objects, date_pointage = date_debut, raison_pointage='employe')
        poitage_employee.save()
        messages.success(request, "presence de l'employe a été bien indiqué") 
    else:

        messages.error(request, "Erreur d'indiquer la presence")

   
    
    return redirect('list_employe_absent')
        

@login_required(login_url="/login/")
def list_employe_present(request):
    context = {}
    context['etat'] = 'present'
    context['segment'] = 'poinatge'
    list_employe = []
    date_debut = datetime.today()
    list_pointage = Pointage.objects.filter(raison_pointage='employe').filter(date_pointage__year=date_debut.year, date_pointage__month=date_debut.month, date_pointage__day=date_debut.day )
    for p in list_pointage:
        list_employe.append(Employes.objects.get(id = p.employe.id))
    
    print("*****************",list_employe, "*****************")
    context['list_employe'] = list_employe


    return render(request, 'pointage.html', context)
@login_required(login_url="/login/")
def list_enfant_present(request):
    context = {}
    context['etat'] = 'present'
    context['segment'] = 'poinatge'
    list_enfant = []
    date_debut = datetime.today()
    list_pointage = Pointage.objects.filter(raison_pointage='enfant').filter(date_pointage__year=date_debut.year, date_pointage__month=date_debut.month, date_pointage__day=date_debut.day )
    for p in list_pointage:
        list_enfant.append(Enfant.objects.get(id = p.enfant.id))

    print("*****************",list_enfant, "*****************")
    context['list_enfant'] = list_enfant


    return render(request, 'pointage-enfant.html', context)



@login_required(login_url="/login/")
def list_employe_absent(request):

    context = {}
    context['etat'] = 'absent'
    context['segment'] = 'poinatge'
    list_id_employe = []
    date_debut = datetime.today()
    list_pointage = Pointage.objects.filter(raison_pointage='employe').filter(date_pointage__year=date_debut.year, date_pointage__month=date_debut.month, date_pointage__day=date_debut.day )
    list_employe_tout = Employes.objects.all().order_by('updated_at')
    for p in list_pointage:
        list_id_employe.append(p.employe.id)
    list_employe = Employes.objects.exclude(id__in=list_id_employe)

    print("*****************",list_employe, "*****************")
    context['list_employe'] = list_employe
    return render(request, 'pointage.html', context)
@login_required(login_url="/login/")
def list_enfant_absent(request):

    context = {}
    context['etat'] = 'absent'
    context['segment'] = 'poinatge'
    list_id_enfant = []
    date_debut = datetime.today()
    list_pointage = Pointage.objects.filter(raison_pointage='enfant').filter(date_pointage__year=date_debut.year, date_pointage__month=date_debut.month, date_pointage__day=date_debut.day )
    list_enfant_tout = Enfant.objects.all().order_by('updated_at')
    for p in list_pointage:
        list_id_enfant.append(p.enfant.id)
    list_enfant = Enfant.objects.exclude(id__in=list_id_enfant)

    print("*****************",list_enfant, "*****************")
    context['list_enfant'] = list_enfant
    return render(request, 'pointage-enfant.html', context)




@login_required(login_url="/login/")
def supprimer_pointage(request):
    context = {}
    date_debut = datetime.today()
    context['etat'] = 'absent'
    context['segment'] = 'poinatge'
    if request.method == "POST":
        id_employe = request.POST.get('employe')
        
    try:
        Pointage.objects.filter(raison_pointage='employe').filter(date_pointage__year=date_debut.year, date_pointage__month=date_debut.month, date_pointage__day=date_debut.day ).filter(employe_id=id_employe).delete()
    except Exception as e:
        print(e)

    
    return redirect('list_employe_absent')
@login_required(login_url="/login/")
def supprimer_pointage_enfant(request):
    context = {}
    date_debut = datetime.today()
    context['etat'] = 'absent'
    context['segment'] = 'poinatge'
    if request.method == "POST":
        id_enfant = request.POST.get('enfant')
        
    try:
        Pointage.objects.filter(raison_pointage='enfant').filter(date_pointage__year=date_debut.year, date_pointage__month=date_debut.month, date_pointage__day=date_debut.day ).filter(enfant_id=id_enfant).delete()
    except Exception as e:
        print(e)

    
    return redirect('list_enfant_absent')



@login_required(login_url="/login/")
def pointage_employe(request):
    context = {}
    context['segment'] = 'employe'
    if request.method == "POST":
        id_employe = request.POST.get('employe')

    context['list_pointage_employe'] = Pointage.objects.filter(employe_id=id_employe)
    context['nb_presence'] = Pointage.objects.filter(employe_id=id_employe).count()
    context['employe']= Employes.objects.get(id = id_employe)
    
    return render(request, 'liste-pointage-employe.html', context)

@login_required(login_url="/login/")
def pointage_enfant(request):
    context = {}
    context['segment'] = 'enfant'
    if request.method == "POST":
        id_enfant = request.POST.get('enfant')

    context['list_pointage_enfant'] = Pointage.objects.filter(enfant_id=id_enfant)
    context['nb_presence'] = Pointage.objects.filter(enfant_id=id_enfant).count()
    context['enfant']= Enfant.objects.get(id = id_enfant)
    
    return render(request, 'liste-pointage-enfant.html', context)



@login_required(login_url="/login/")
def imprimer_pointage_enfant(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",12)
    if request.method =="POST":
        date_fin_pointage = request.POST.get('date_fin_pointage')
        date_debut_pointage = request.POST.get('date_debut_pointage')
        jour = request.POST.get('jour')
        id_enfant = request.POST.get('enfant')

    date_debut_poin = dt.datetime.strptime(date_debut_pointage, '%Y-%m-%d')
    date_fin_poin = dt.datetime.strptime(date_fin_pointage, '%Y-%m-%d')
    print(date_fin_poin-date_debut_poin)
    creche = Creche.objects.get(id = Creche.objects.last().id)
    enfant = Enfant.objects.get(id = id_enfant)
    nom_creche = creche.nom
    adresse_creche = creche.adresse
    
    c.drawString(70,230 , nom_creche)
    c.drawString(70,250, adresse_creche)
    list_date = pandas.date_range(date_debut_poin,date_fin_poin-timedelta(days=1),freq='d')
    newList = []
    for x in range (len(list_date)-2):
        newList.append(list_date[x])
   
    print(newList)
    y = 365
    c.drawString(180,343,'Enfant')
    for x in range(5):
        print(newList[x])
        p = Pointage.objects.filter(created_at = newList[x]).filter(enfant_id=id_enfant)
        print(p)
        if p :
            c.drawString(340,y, "present")
        else :

            c.drawString(340,y, "absent")


        c.drawString(180,y, enfant.nom+' '+ enfant.prenom)
        c.drawString(70,y, newList[x].strftime("%m/%d/%Y"))
        y= y+25
        

    c.showPage()
    c.save()
    buf.seek(0)
    new_pdf = PdfFileReader(buf)
    output = PdfFileWriter()
    existing_pdf = PdfFileReader(open("model-pointage.pdf", "rb"))
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    outputStream = open("destination2.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    
    

    return FileResponse(open("destination2.pdf", 'rb'), content_type='application/pdf')







