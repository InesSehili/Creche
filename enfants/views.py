from re import S
from django.shortcuts import render ,redirect
from enfants.models import Enfant
from categoriesAbonnement.models import  CategorieAbonnement
from factures.forms import FactureForm
from parents.forms import ParentForm 
from supplement.models import Supplement 
from autorisations.models import Autorisation
from parents.models import Parent
from classes.models import Classe
from factures.models import Facture
import decimal
from django.contrib import messages

from enfants.forms import EnfantForm

from sectionsage.models import SectionAge
from factureenfants.models import FactureEnfant
from django.contrib.auth.decorators import login_required
from  payement.views import Payement
# Create your views here.



@login_required(login_url="/login/")
def  liste_enfants(request):
    context = {}
    context['segment'] = 'enfant'
    context['list_Enfants'] = Enfant.objects.all().order_by('updated_at')
    


    return render(request, 'liste-enfants.html',context)
@login_required(login_url="/login/")
def  ajouter_enfant(request):
    context = {}
    context['segment'] = 'enfant'
    context['list_Enfants'] = Enfant.objects.all().order_by('updated_at')
    context['list_categories'] =CategorieAbonnement.objects.all().order_by('updated_at')
    context['list_supplement'] =Supplement.objects.all().order_by('updated_at')
    context['list_autorisation'] =Autorisation.objects.all().order_by('updated_at')
    context['list_classe'] = Classe.objects.all().order_by('updated_at')
    

    return render(request, 'ajouter-enfant.html',context)
@login_required(login_url="/login/")
def  valider_ajouter_enfant(request):

    context ={}
  
    if request.method =="POST" :
        #récuperation infos 

        pere = request.POST.get('pere')
        mere = request.POST.get('mere')
        tele_pere  = request.POST.get('telephone_pere')
        tele_mere  = request.POST.get('telephone_mere')
        etat = request.POST.get('etat')
        email  = request.POST.get('email')
        personne_autorise = request.POST.get('personne_autorise')  
        adresse  = request.POST.get('adresse')  

        #enregistremenet parent
        # parent = Parent(pere=pere, mere=mere, adresse =adresse ,telephone_pere = tele_pere, telephone_mere = tele_mere, etat =etat, email = email, personne_autorise= personne_autorise)
        # parent.save()


        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        age = request.POST.get('age')
        sexe = request.POST.get('sexe')
        nombre_frere = request.POST.get('nombre_frere')

        categorie_prix = request.POST.get("categorie")
        categorie = categorie_prix.split()[0]


        suplement = request.POST.getlist("suplement[]")

        autoristation = request.POST.getlist("autorisation[]")

        client = request.POST.get("client")
        mois = request.POST.get("mois")
        frais_inscription =decimal.Decimal( request.POST.get("frais_inscription"))
        prix_paye = decimal.Decimal(request.POST.get("prix_paye"))
        classe = request.POST.get('classe')

        form = EnfantForm(request.POST , request.FILES)
        context['form'] = form
        formP =ParentForm(request.POST , request.FILES)
        context['formP'] =formP
        formF =FactureForm(request.POST , request.FILES)
        context['formF'] =formF
        
        prix_categorie = 0 
        prix_supplement = 0
        
        if categorie : 
            categorieAbonnement = CategorieAbonnement.objects.get(id = categorie)
            prix_categorie = categorieAbonnement.prix
       
        
        classe = request.POST.get('classe')
        

        if suplement : 
            for i in range(len(suplement)):
                sup = suplement[i].split()[0]
                obj_supplement = Supplement.objects.get(id=decimal.Decimal(sup))
                prix_supplement = prix_supplement + obj_supplement.prix
        total_payement = frais_inscription + prix_categorie + prix_supplement 
        rest_paye =  total_payement - prix_paye
        print("***********" , rest_paye)
        print("***********" , prix_paye)

        # if frais_inscription >= 0 :
        #     if prix_paye >= 0 :
        if prix_paye <= total_payement :



                        
            parent = Parent(pere=pere, mere=mere, adresse =adresse ,telephone_pere = tele_pere , telephone_mere = tele_mere, etat =etat , email = email,personne_autorise = personne_autorise)
            parent.save()
                        
            classeO = Classe.objects.get(id =classe)
            nbr_enfant = classeO.nbr_enfant
            Classe.objects.filter(id = classe).update(nbr_enfant = nbr_enfant + 1)
            if 'image' in request.FILES :
                image = request.FILES['image']
                enfant = Enfant(nom= nom, prenom = prenom, date_naissance = date_naissance, age = age, sexe = sexe, parents=parent,  classe= classeO , image=image ,prix_paye =prix_paye , reste_paye = rest_paye , total_payement = total_payement )
                enfant.save(force_insert=True)
                facture_enfant = FactureEnfant(enfant=enfant,categorie=categorieAbonnement,client = client, frais_inscription=frais_inscription, prix_paye =prix_paye , reste_paye = rest_paye , prix_total = total_payement )
                facture_enfant.save()
                payement_enfant = Payement(enfant = enfant , facture = facture_enfant , prix_payer = prix_paye , client = client,  reste_facture_apres_ce_paiment = rest_paye )
                payement_enfant.save()
                if suplement : 
                    for i in range(len(suplement)):
                        sup = suplement[i].split()[0]
                        obj_supplement = Supplement.objects.get(id=decimal.Decimal(sup))
                        prix_supplement = prix_supplement + obj_supplement.prix
                        if(True):
                            facture_enfant.supplement.add(obj_supplement)
    
                if autoristation :
                    for i in range(len(autoristation)):
                         obj_autorisation= Autorisation.objects.get(id=autoristation[i])   
                         if(True):
                            enfant.autorisation.add(obj_autorisation)
                
                          
                messages.info(request, "l'enfant ainsi sa facture ont été bien enregistré")         
            else :


                                    
                enfant = Enfant(nom= nom, prenom = prenom , date_naissance = date_naissance , age = age , sexe = sexe,parents=parent, classe= classeO ,prix_paye =prix_paye , reste_paye = rest_paye , total_payement = total_payement )
                enfant.save(force_insert=True)
                facture_enfant = FactureEnfant(enfant=enfant,categorie=categorieAbonnement,client=client ,frais_inscription=frais_inscription, prix_paye =prix_paye , reste_paye = rest_paye , prix_total = total_payement )
                facture_enfant.save()
                payement_enfant = Payement(enfant = enfant , facture = facture_enfant , prix_payer = prix_paye , client = client, reste_facture_apres_ce_paiment = rest_paye )
                payement_enfant.save()
                if suplement :
                    for i in range(len(suplement)):
                        sup = suplement[i].split()[0]
                        obj_supplement = Supplement.objects.get(id=decimal.Decimal(sup))
                        prix_supplement = prix_supplement + obj_supplement.prix
                        if(True):

                            facture_enfant.supplement.add((obj_supplement))
                        
                if autoristation :

                    for i in range(len(autoristation)):


                        obj_autorisation= Autorisation.objects.get(id=autoristation[i])   
                        if(True):
                            enfant.autorisation.add(obj_autorisation)
                                    
                messages.info(request, "l'enfant ainsi sa facture ont été bien enregistré")    
        else :
            messages.error(request,'Le prix payé doit etre superieur ou egal  du reste ')
            context['list_categories'] =CategorieAbonnement.objects.all().order_by('updated_at')
            context['list_supplement'] =Supplement.objects.all().order_by('updated_at')
            context['list_autorisation'] =Autorisation.objects.all().order_by('updated_at')
            context['list_classe'] = Classe.objects.all().order_by('updated_at')
            return render(request, 'ajouter-enfant.html' , context)
                    
        return redirect('ajouter_enfant')

            

        
        

@login_required(login_url="/login/")
def afficher_detail_enfant(request):
    context = {}
    if request.method =="POST":
        id = request.POST.get("id")
        enfant = Enfant.objects.get(id=id)
        context ["nom"] =enfant.nom
        context ["prenom"] =enfant.prenom
        context ["date_naissance"] =enfant.date_naissance
        context ["age"] =enfant.age
        context ["sexe"] =enfant.sexe
      
        if enfant.classe :

            context ["classe"] =enfant.classe.nom_classe
        else :

            context ["classe"] = " "  
        context ["prix_paye"] =enfant.prix_paye

        context ["reste_paye"] =enfant.reste_paye
        context ["total_payement"] =enfant.total_payement
  
        context["enfant"] = enfant
        context ["pere"] =enfant.parents.pere
        context ["mere"] =enfant.parents.mere
        context ["adresse"] =enfant.parents.adresse
        context ["telephone_pere"] =enfant.parents.telephone_pere
        context ["telephone_mere"] =enfant.parents.telephone_mere
        context ["etat"] =enfant.parents.etat
        context ["email"] =enfant.parents.email
        context ["personne_autorise"] =enfant.parents.personne_autorise 
        if  enfant.autorisation :  
            context['list_autorisation'] = enfant.autorisation.all()
        else :
           context['list_autorisation'] = " "     
        context['image'] = enfant.get_image

    return render(request, 'afficher-detail-enfant.html' , context)
@login_required(login_url="/login/")
def supprimer_enfant(request):
    
    if request.method =="POST":
        enfant = request.POST.get("id")      
        enfantt = Enfant.objects.get(id=enfant)
        classe_id = enfantt.classe.id
        classe_nb_enfant = enfantt.classe.nbr_enfant
        classe_nb_enfant =classe_nb_enfant - 1
        Classe.objects.filter(id = classe_id).update(nbr_enfant = classe_nb_enfant)
        Enfant.objects.get(id=enfant).delete()
    return redirect('liste_enfants')
@login_required(login_url="/login/")
def modifier_enfant(request):
    context = {}    
    if request.method =="POST":
        id_enfant = request.POST.get("id")
        enfant = Enfant.objects.get(id=id_enfant)
        context ['enfant'] =enfant
       
        
    context['list_classe'] = Classe.objects.all().order_by('updated_at')
    list_autorisation = []
    list_autorisationc = enfant.autorisation.all()
    
    for aut in list_autorisationc :
        list_autorisation.append(aut.id)

    list_autorisation2 = Autorisation.objects.exclude(id__in=list_autorisation)    
    context['list_autorisation'] =list_autorisation2
    context['list_autorisationc'] = enfant.autorisation.all()

    return render(request, 'modifier-enfant.html', context)
@login_required(login_url="/login/")
def valider_modifier_enfant(request):
    
    if request.method == 'POST' :
        id = request.POST.get('id_enfant')
        print("id enfant ", id)
        pere = request.POST.get('pere')
        mere = request.POST.get('mere')
        tele_pere  = request.POST.get('telephone_pere')
        tele_mere   = request.POST.get('telephone_mere')
        etat = request.POST.get('etat')
        email  = request.POST.get('email')
        personne_autorise = request.POST.get('personne_autorise')  
        adresse  = request.POST.get('adresse')

        enfant = Enfant.objects.get(id = id)
        id_parent = enfant.parents.id
        print("id parent : " , id_parent)


        Parent.objects.filter(id = id_parent).update(pere = pere)
        Parent.objects.filter(id = id_parent).update(mere = mere)
        Parent.objects.filter(id = id_parent).update(telephone_pere= tele_pere)
        Parent.objects.filter(id = id_parent).update(telephone_mere =tele_mere)
        Parent.objects.filter(id = id_parent).update(etat= etat)
        Parent.objects.filter(id = id_parent).update(email= email)
        Parent.objects.filter(id = id_parent).update(personne_autorise = personne_autorise)
        Parent.objects.filter(id = id_parent).update(adresse = adresse)
        
        

        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        age = request.POST.get('age')
        sexe = request.POST.get('sexe')
       
        autoristation = request.POST.getlist("autorisation[]")

        if 'image' in request.FILES :
            image = request.FILES['image']
            Enfant.objects.filter(id = id).update(image =  image)
        else :
            print ("yes")
        classe = request.POST.get("classe")
        
        Enfant.objects.filter(id = id).update(nom = nom)
        Enfant.objects.filter(id = id).update(prenom = prenom)
        if date_naissance :
           Enfant.objects.filter(id = id).update(date_naissance = date_naissance)
        Enfant.objects.filter(id = id).update(age = age)
        Enfant.objects.filter(id = id).update(sexe = sexe)
     
        
        if enfant.classe : 
            if classe == enfant.classe.id : 
                Enfant.objects.filter(id = id).update(classe = classe)
            else : 
                classeO = Classe.objects.get(id =classe)
                nbr_enfant = classeO.nbr_enfant
                Classe.objects.filter(id = classe).update(nbr_enfant = nbr_enfant + 1)
                id_classe_der = enfant.classe.id
                classe1 =Classe.objects.get(id = id_classe_der)
                nbr_enfant1 = classe1.nbr_enfant
                Classe.objects.filter(id = id_classe_der).update(nbr_enfant = nbr_enfant1 - 1)
                Enfant.objects.filter(id = id).update(classe = classe)   
        else : 
            classeO = Classe.objects.get(id =classe)
            nbr_enfant = classeO.nbr_enfant
            Classe.objects.filter(id = classe).update(nbr_enfant = nbr_enfant + 1)
            Enfant.objects.filter(id = id).update(classe = classe)
        
        
       
        enfant.autorisation.clear()
       
        if autoristation :
            for i in range(len(autoristation)):

                obj_autorisation= Autorisation.objects.get(id=autoristation[i])
                
                if(True):
                    enfant.autorisation.add(obj_autorisation)
        messages.info(request, 'enfant a été bien modifie')

    return redirect('liste_enfants')