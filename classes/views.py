from django.shortcuts import redirect, render

from classes.models import Classe
from classes.ClasseForm import ClasseForm,form_validation_error
from employes.models import Employes
from django.contrib import messages
import datetime as dt
from factureenfants.models import FactureEnfant
from datetime import datetime, timezone
from enfants.models import Enfant
from payement.models import Payement

# Create your views here.
from django.contrib.auth.decorators import login_required
@login_required(login_url="/login/")
def liste_classes(request):
    context = {}
    context['segment'] = 'classe'
    context['liste_classes'] = Classe.objects.all().order_by('updated_at')
    context['list_employee'] = Employes.objects.filter(fonction='educatrice')
    if request.method =='POST':
        form = ClasseForm(request.POST or None)
        if form.is_valid():
            print("form is valid")
            form.save()
            messages.success(request, 'classe a ete bien ajoute')
            context['liste_classes'] = Classe.objects.all().values().order_by("created_at").reverse()
            return redirect('liste_classes')
        else:
            print("form is not valid")
            messages.error(request,form_validation_error(form))
    

    return render(request, 'liste-classes.html',context)

# Create your views here.
@login_required(login_url="/login/")
def modifier_classe(request):
    context = {}
    context['segment'] = 'classe'
    if request.method =="POST":
        idclasse = request.POST.get("id")
        classe = Classe.objects.get(id=idclasse)
        context ['classe'] = classe
        
    context['list_employee'] = Employes.objects.filter(fonction='educatrice')
    
    return render(request, 'modifier_classe.html', context)

# Create your views here.
@login_required(login_url="/login/")
def update_classe(request):
    
    if request.method == 'POST':
        id_classe = request.POST.get("id")
        id_employe = request.POST.get("employe")
        nom_classe = request.POST.get("nom_classe")
        niveau = request.POST.get("niveau")
        nbr_enfant = request.POST.get('nbr_enfant')
        
        
        Classe.objects.filter(id = id_classe).update(employe=id_employe)
        Classe.objects.filter(id = id_classe).update(nom_classe=nom_classe)
        if niveau :
             Classe.objects.filter(id = id_classe).update(niveau=niveau)
        Classe.objects.filter(id = id_classe).update(nbr_enfant=nbr_enfant)
        
        messages.info(request, 'Classe a été bien modifie')
    
    
    return redirect('liste_classes')
# Create your views here.
@login_required(login_url="/login/")
def supprimer_classes(request):
    
    if request.method =="POST":
        classe = request.POST.get("id")
        print("classe = ", classe)
    
    Classe.objects.get(id=classe).delete()
    messages.info(request, 'Classe a été bien supprimer')
    
    return redirect('liste_classes')

@login_required(login_url="/login/")
def voir_revenu_par_classe(request):

    context = {}
    revenu_entre = 0
    context['segment'] = 'classe'
    context['liste_classes'] = Classe.objects.all().order_by('updated_at')
    context['list_employee'] = Employes.objects.filter(fonction='educatrice')
    list_facture = []
    list_facture2 = []
    if request.method =="POST":
        classe = request.POST.get('classe')
        date_debut_str = request.POST.get('date_debut')
        date_fin_str = request.POST.get('date_fin')
    date_debut = dt.datetime.strptime(date_debut_str, '%Y-%m-%d')
    date_fin = dt.datetime.strptime(date_fin_str, '%Y-%m-%d')
    classe_obj = Classe.objects.get(id =classe)
    list_enfant = Enfant.objects.filter(classe = classe_obj)
    if date_debut > date_fin:
        messages.error(request, "Date de debut ou de fin erroné")
    else :
        for enf in list_enfant:
            list_facture2 = Payement.objects.filter(enfant = enf).filter(created_at__date__range=[date_debut, date_fin])

        for f in list_facture2:
            list_facture.append(f)

        print(list_facture)

        if len(list_facture) !=0:
            for payement in list_facture:
                revenu_entre = revenu_entre + payement.prix_payer
        context['revenu_entre'] = revenu_entre

    return render(request, 'liste-classes.html',context)




