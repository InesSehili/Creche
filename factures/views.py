
from django.shortcuts import redirect, render
from employes.models import Employes
from factures.forms import FactureForm ,form_validation_error
from factures.models import Facture
from django.contrib import messages
from enfants.models import Enfant
from categoriesAbonnement.models import CategorieAbonnement
from supplement.models import Supplement 
import decimal
from prixsortie.models import Prixsortie
from django.contrib.auth.decorators import login_required
# Create your views here.
# def liste_factures(request):
#     context = {}
#     context['segment'] = 'facture'
#     context['list_factures'] = Facture.objects.all().order_by('updated_at')
#     return render(request, 'paiements.html',context)

# def ajouter_paiement_mensuelle(request):
#     context ={}
#     context['list_enfants'] = Enfant.objects.all().order_by('updated_at')
#     context['list_categories'] =CategorieAbonnement.objects.all().order_by('updated_at')
#     context['list_supplement'] =Supplement.objects.all().order_by('updated_at')

#     return render(request, 'ajouter-paiement-enfant.html' ,context)

# def liste_factures_enfant(request):
#     context={}
#     context['segment'] = 'enfant'
#     if request.method =="POST": 
#         id_enfant = request.POST.get('enfant')


#     enfant = Enfant.objects.get(id=id_enfant)
#     context['list_factures'] = Facture.objects.filter(employe=None).filter(enfant=enfant).order_by('updated_at')
#     return render(request, 'paiements.html',context)


# liste de paiement pour chaque  employe
@login_required(login_url="/login/")
def liste_factures_employe(request):
    context={}
    context['segment'] = 'paiemente'
    if request.method =="POST":
        id_employe = request.POST.get('employe')
   
    employes = Employes.objects.get(id=id_employe)
    context['employe'] =  employes
    context['list_factures'] = Facture.objects.filter(enfant=None).filter(employe=employes).order_by('updated_at')
    return render(request, 'paiement-employe.html',context)

# liste de paiement pour tous les employe
@login_required(login_url="/login/")
def paiement_employe(request):
    context={}
    context['segment'] = 'paiemente'
    
    context['list_factures'] = Facture.objects.filter(enfant=None)
    return render(request, 'paiement-employe.html',context)


# valider l'ajoute de paiement employe
@login_required(login_url="/login/")
def ajouter_paiement_employe(request):
        context = {}
        context['list_factures'] = Facture.objects.filter(enfant=None)
        if request.method =="POST":
            prix = request.POST.get('tarif')
            date = request.POST.get('date')
            form = FactureForm(request.POST or None)
            if form.is_valid():
                print("form is valid")
                form.save()
                last_facture = Facture.objects.last()
                prixsortie=Prixsortie(facture=last_facture ,prix_sortie = decimal.Decimal(prix) , raison_payement = 'employe' , date = date)
                prixsortie.save(force_insert=True)

                messages.success(request, 'Facture a été bien crée')
            
            else:


                messages.error(request,form_validation_error(form))
        return  render(request, 'paiement-employe.html',context)          

# supprimer facture employe 
@login_required(login_url="/login/")
def supprimer_facture(request):    
    if request.method =="POST":
        facture = request.POST.get("facture")
        print("facture = ", facture)       
        tarif = request.POST.get("tarif")
        tar = decimal.Decimal(tarif)
        Facture.objects.get(id=facture).delete()
        messages.info(request, 'Facture employe a ete bien supprimer ')

    
    return redirect('paiement_employe')
# modifier facture employe 
@login_required(login_url="/login/")
def modifier_facture(request):
    context = {}
    if request.method =="POST":
        id_facture = request.POST.get("facture")
        facture = Facture.objects.get(id=id_facture)
        context['facture'] =facture    


    return  render(request, 'modifier-paiements.html',context) 
#valider modifier facture 
@login_required(login_url="/login/")
def valider_modifier_facture_employe(request) :
    if request.method =="POST":
        id_employe =  request.POST.get("employe")  
        employe =Employes.objects.get(id = id_employe)         
        tarif = request.POST.get("tarif")
        id_facture = request.POST.get("facture")
        date = request.POST.get("date")
          
        Facture.objects.filter(id = id_facture).update(tarif = tarif)
        Facture.objects.filter(id = id_facture).update(employe = employe)
        if date :
          Facture.objects.filter(id = id_facture).update(date = date)
          Prixsortie.objects.filter(facture_id = id_facture).update(date = date)

        Prixsortie.objects.filter(facture_id = id_facture).update(prix_sortie = tarif)
        messages.info(request, 'Facture employe a ete bien modifier ')

    return redirect('paiement_employe')    











# def valider_paiement_mensuelle(request) :
#     if request.method =="POST":
#         context ={}
#         id_enfant =  request.POST.get("enfant")  
#         enfant =Enfant.objects.get(id = id_enfant)  
#         client =  request.POST.get("client")  
#         mois = request.POST.get("mois")
#         prix_paye  = decimal.Decimal(request.POST.get("prix_paye"))
#         tarif =  decimal.Decimal(request.POST.get("tarif")) 
#         id_categorie = request.POST.get("categorie")
#         categorie = CategorieAbonnement.objects.get(id= id_categorie)
#         prix_categorie = decimal.Decimal(categorie.prix)
#         list_sup = request.POST.getlist("suplement[]")
        
        
#         enfant.supplement.clear()
#         prix_supplement = 0
#         if list_sup : 
#                     for i in range(len(list_sup)):
#                         obj_supplement = Supplement.objects.get(id=list_sup[i])
#                         prix = decimal.Decimal(obj_supplement.prix)
#                         prix_supplement = prix_supplement + prix
#                         if(True):
#                             enfant.supplement.add((obj_supplement))    

#         total_payement_auj = tarif + prix_categorie + prix_supplement 
#         total_payement_pre = enfant.total_payement
#         total_payement = total_payement_auj + total_payement_pre
                    
#         prix_paye_pre = enfant.prix_paye
#         total_prix_paye = prix_paye_pre + prix_paye
            
#                 # reste_paye_pre = enfant.reste_paye
#                 # reste_paye_auj = total_payement_auj - prix_paye
#         rest_paye = total_payement - total_prix_paye

#         if prix_paye <= rest_paye :    
#                         Enfant.objects.filter(id = id_enfant).update(prix_paye = total_prix_paye)
#                         Enfant.objects.filter(id = id_enfant).update(reste_paye = rest_paye)
#                         Enfant.objects.filter(id = id_enfant).update(total_payement = total_payement)
#                         Enfant.objects.filter(id = id_enfant).update(categorie = id_categorie)
                        
#                         facture = Facture (enfant = enfant , tarif = prix_paye , client = client , mois = mois ,frais_inscription =tarif )
#                         facture.save(force_insert=True)
#                         messages.success(request, 'Facture a ete bien cree ')

#                         context ={}
#                         context['list_enfants'] = Enfant.objects.all().order_by('updated_at')
#                         context['list_categories'] =CategorieAbonnement.objects.all().order_by('updated_at')
#                         context['list_supplement'] =Supplement.objects.all().order_by('updated_at')
#                         context['rest_paye'] = rest_paye
#                         context['total_payement'] = total_payement
#                         context['prix_paye'] = total_prix_paye
#         else :
#                     messages.error(request,'prix paye doit étre plus que reste de payement ')
#                     formF =FactureForm(request.POST , request.FILES)
#                     context['form'] =formF
#                     context['list_enfants'] = Enfant.objects.all().order_by('updated_at')
#                     context['list_categories'] =CategorieAbonnement.objects.all().order_by('updated_at')
#                     context['list_supplement'] =Supplement.objects.all().order_by('updated_at')

#                     return render(request, 'ajouter-paiement-enfant.html' ,context)                           
#     return redirect('ajouter_paiement_mensuelle')





# def ajouter_paiement_employes(request):
#     context = {}
#     context['list_employee'] = Employes.objects.all().values().order_by('updated_at')
#     return render(request, 'ajouter-paiement-employes.html',context)




# def modifier_facture(request):
#     context = {}
#     if request.method =="POST":
#         id_facture = request.POST.get("facture")
#         facture = Facture.objects.get(id=id_facture)
#         context['facture'] =facture

#         if facture.enfant == None : 
#             context['client'] = 'employe'
#             employe = facture.employe
#             context['employe'] = employe

#         else :
#             context['client'] = 'enfant'
#             enfant = facture.enfant
#             context['enfant'] = enfant
#             context['list_enfants'] = Enfant.objects.all().order_by('updated_at')
#             context['list_categories'] =CategorieAbonnement.objects.all().order_by('updated_at')
#             context['list_supplement'] =Supplement.objects.all().order_by('updated_at')
#             list_supplement = []
#             list_supplement_enfant = enfant.supplement.all()
#             for supp in list_supplement_enfant :
#                 list_supplement.append(supp.id)
#             list_supplement_autre = Supplement.objects.exclude(id__in=list_supplement)
#             context['list_supplement_autre'] =list_supplement_autre
#             context['list_supplement_enfant'] = enfant.supplement.all()
  

#     return  render(request, 'modifier-paiements.html',context) 

# def valider_modifier_facture_enfant(request) :
#     context = {}
#     if request.method =="POST":
#         id_enfant =  request.POST.get("enfant")  
#         enfant =Enfant.objects.get(id = id_enfant)  
#         client =  request.POST.get("client")  
#         mois = request.POST.get("mois")
#         prix_paye_new  = decimal.Decimal(request.POST.get("prix_paye"))
#         tarif = request.POST.get("tarif")
#         id_categorie = request.POST.get("categorie")
#         categorie = CategorieAbonnement.objects.get(id= id_categorie)
#         prix_categorie = decimal.Decimal(categorie.prix)
#         list_sup = request.POST.getlist("suplement[]")
#         id_facture = request.POST.get("facture")
#         facture = Facture.objects.get(id=id_facture)
        
#         prix_pre = facture.tarif
#         frais_ins_prec = facture.frais_inscription

#         total_payement_pre = enfant.total_payement
#         prix_paye_pre = enfant.prix_paye
#         prix_categorie_pre =enfant.categorie.prix
#         supplement_prec = enfant.supplement.all()
#         prix_supp_prec= 0
#         for sup in supplement_prec :
#             prix_supp_prec = prix_supp_prec + sup.prix

#         total_payement_pre = total_payement_pre - prix_categorie_pre - prix_supp_prec - frais_ins_prec

#         enfant.supplement.clear()
#         prix_supplement = 0
#         if list_sup : 
#             for i in range(len(list_sup)):
#                 obj_supplement = Supplement.objects.get(id=list_sup[i])
#                 prix = decimal.Decimal(obj_supplement.prix)
#                 prix_supplement = prix_supplement + prix
#                 if(True):
#                     enfant.supplement.add((obj_supplement)) 
         
        
#         prix_paye_ajout = (prix_paye_pre - prix_pre) + prix_paye_new        
#         tarif =decimal.Decimal(tarif)
#         total_payement_new = total_payement_pre + tarif + prix_categorie + prix_supplement
           

#         rest_paye = total_payement_new - prix_paye_ajout
#         if rest_paye >= prix_paye_ajout :
#             Enfant.objects.filter(id = id_enfant).update(prix_paye = prix_paye_ajout)
#             Enfant.objects.filter(id = id_enfant).update(reste_paye = rest_paye)
#             Enfant.objects.filter(id = id_enfant).update(total_payement = total_payement_new)
#             Enfant.objects.filter(id = id_enfant).update(categorie = id_categorie)


#             Facture.objects.filter(id = id_facture).update(tarif = prix_paye_new)
#             Facture.objects.filter(id = id_facture).update(client = client)
#             Facture.objects.filter(id = id_facture).update(mois = mois)
#             Facture.objects.filter(id = id_facture).update(frais_inscription = tarif)
#             messages.info(request, 'Facture enfant a ete bien modifier ')
#         else :
#             formF =FactureForm(request.POST , request.FILES)
#             context['form'] =formF
#             id_facture = request.POST.get("facture")
#             facture = Facture.objects.get(id=id_facture)
#             context['facture'] =facture
#             context['client'] = 'enfant'
#             enfant = facture.enfant
#             context['enfant'] = enfant
#             context['list_enfants'] = Enfant.objects.all().order_by('updated_at')
#             context['list_categories'] =CategorieAbonnement.objects.all().order_by('updated_at')
#             context['list_supplement'] =Supplement.objects.all().order_by('updated_at')
#             list_supplement = []
#             list_supplement_enfant = enfant.supplement.all()
#             for supp in list_supplement_enfant :
#                 list_supplement.append(supp.id)
#             list_supplement_autre = Supplement.objects.exclude(id__in=list_supplement)
#             context['list_supplement_autre'] =list_supplement_autre
#             context['list_supplement_enfant'] = enfant.supplement.all()
#             messages.error(request,'prix paye doit étre plus que reste de payement ')
#             return  render(request, 'modifier-paiements.html',context) 
       
#         context['list_factures'] = Facture.objects.all().values().order_by('updated_at')

#     return redirect('liste_factures')

