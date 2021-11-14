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
from datetime import date, timedelta , timezone


# Create your views here.
@login_required(login_url="/login/")
def ajouter_pointage_enfant(request):
    context = {}
    
    context['segment'] = 'poinatge'
    date_debut_a = datetime.today()
    date_debut = date_debut_a.date()

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
    date_debut_a = datetime.today()
    date_debut = date_debut_a.date()

    
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
    date_debut_a = datetime.today()
    date_debut = date_debut_a.date()

    list_pointage = Pointage.objects.filter(raison_pointage='employe').filter(date_pointage=date_debut )
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
    date_debut_a = datetime.today()
    date_debut = date_debut_a.date()
    list_pointage = Pointage.objects.filter(raison_pointage='enfant').filter(date_pointage=date_debut )
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
    date_debut_a = datetime.today()
    date_debut = date_debut_a.date()
    list_pointage = Pointage.objects.filter(raison_pointage='employe').filter(date_pointage=date_debut)
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
    date_debut_a = datetime.today()
    date_debut = date_debut_a.date()
    list_pointage = Pointage.objects.filter(raison_pointage='enfant').filter(date_pointage=date_debut )
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
    date_debut_a = datetime.today()
    date_debut = date_debut_a.date()
    context['etat'] = 'absent'
    context['segment'] = 'poinatge'
    if request.method == "POST":
        id_employe = request.POST.get('employe')
        
    try:
        Pointage.objects.filter(raison_pointage='employe').filter(date_pointage =date_debut ).filter(employe_id=id_employe).delete()
    except Exception as e:
        print(e)

    
    return redirect('list_employe_absent')
@login_required(login_url="/login/")
def supprimer_pointage_enfant(request):
    context = {}
    date_debut_a = datetime.today()
    date_debut = date_debut_a.date()
    context['etat'] = 'absent'
    context['segment'] = 'poinatge'
    if request.method == "POST":
        id_enfant = request.POST.get('enfant')
        
    try:
        Pointage.objects.filter(raison_pointage='enfant').filter(date_pointage=date_debut ).filter(enfant_id=id_enfant).delete()
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
    gerant = creche.gerant
    adresse_creche = creche.adresse
    
    c.drawString(70,230 , nom_creche)
    c.drawString(70,250, adresse_creche)
    c.drawString(70, 310, gerant)
    c.drawString(178, 310, enfant.parents.pere)
    date_sur_pointage = datetime.now(timezone.utc).strftime("%d/%m/%Y")
    
    c.drawString(315, 310, date_sur_pointage)




    list_date = pandas.date_range(date_debut_poin,date_fin_poin-timedelta(days=1),freq='d')
    newList = []
    nb_date = len(list_date)
    print('longuer de la liste des date = ', nb_date)
    for x in range (nb_date):
        print("element de liste de date = ",list_date[x] )
        newList.append(list_date[x])
    y = 365
    c.drawString(180,343,'Enfant')
    len_co = len(newList)
    print("la longueur de la liste est:", len_co)
    for x in range(len_co):
        print(newList[x])
        p = Pointage.objects.filter(created_at__date__range=[newList[x], newList[x]]).filter(enfant_id=id_enfant)
        print("liste de pointage", p)
        if p.exists() :
            c.drawString(340,y, "present")
        else :

            c.drawString(340,y, "absent")


        c.drawString(180,y, enfant.nom+' '+ enfant.prenom)
        c.drawString(70,y, newList[x].strftime("%d/%m/%Y"))
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

@login_required(login_url="/login/")
def imprimer_pointage_employe(request):

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",12)
    if request.method =="POST":
        date_fin_pointage = request.POST.get('date_fin_pointage')
        date_debut_pointage = request.POST.get('date_debut_pointage')
        jour = request.POST.get('jour')
        id_employe = request.POST.get('employe')

    date_debut_poin = dt.datetime.strptime(date_debut_pointage, '%Y-%m-%d')
    date_fin_poin = dt.datetime.strptime(date_fin_pointage, '%Y-%m-%d')
    print(date_fin_poin-date_debut_poin)
    creche = Creche.objects.get(id = Creche.objects.last().id)
    employe = Employes.objects.get(id = id_employe)
    nom_creche = creche.nom
    gerant = creche.gerant
    adresse_creche = creche.adresse
    
    c.drawString(70,230 , nom_creche)
    c.drawString(70,250, adresse_creche)
    c.drawString(70, 310, gerant)
    c.drawString(165, 310, employe.nom)
    date_sur_pointage = datetime.now(timezone.utc).strftime("%d/%m/%Y")
    
    c.drawString(330, 310, date_sur_pointage)




    list_date = pandas.date_range(date_debut_poin,date_fin_poin-timedelta(days=1),freq='d')
    newList = []
    nb_date = len(list_date)
    print('longuer de la liste des date = ', nb_date)
    for x in range (nb_date):
        print("element de liste de date = ",list_date[x] )
        newList.append(list_date[x])
    y = 365
    y1 = 365
    c.drawString(180,343,'Enfant')
    len_co = len(newList)
    print("la longueur de la liste est:", len_co)
    ligne_de_table = 1
    for x in range(len_co):
        print(newList[x])
        p = Pointage.objects.filter(created_at__date__range=[newList[x], newList[x]]).filter(employe_id=id_employe)
        print("liste de pointage", p)
        if p.exists() :
            if ligne_de_table <= 16:
                c.drawString(340,y, "present")
            else:
                c.drawString(690,y1, "present")

            
        else :
            if ligne_de_table <= 16:
                c.drawString(340,y, "absent")
            else:
                c.drawString(690,y1, "absent")
                

            

        if ligne_de_table <= 16:
            c.drawString(180,y, employe.nom)
            c.drawString(70,y, newList[x].strftime("%d/%m/%Y"))
        else:
            c.drawString(530,y1, employe.nom)
            c.drawString(420,y1, newList[x].strftime("%d/%m/%Y"))
            y1= y1+23


        
        
        y= y+23
        ligne_de_table = ligne_de_table+1
        

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




