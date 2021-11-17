from django.shortcuts import redirect, render
from django.contrib import messages
from prixsortie.models import Prixsortie
from depenses.models import Depense
import decimal
from stock.models import Stock
from besoin.models import Besoin
from django.contrib.auth.decorators import login_required
from employes.models import Employes
from factures.models import Facture
# Create your views here.
@login_required(login_url="/login/")
def liste_depenses(request) :
    context = {}
    context['segment'] = 'depense'
    prixsortie = Prixsortie.objects.all().values() 
    context['liste_depenses'] = prixsortie
    list_facture = []
    total_dep = 0
    
    liste_depenses_filter = Depense.objects.all().values()
    context['liste_depenses_rceherche'] =  liste_depenses_filter      
    if request.method == "POST":
        type_depense = request.POST.get('depense')
        
        if type_depense == '' :
            prixsortie = Prixsortie.objects.all().values()
        else:
            if type_depense == 'educatrice' or type_depense == 'femmedemenage' or type_depense == 'chauffeur' or type_depense == 'cuisinie' or type_depense == 'assistante':
                print("inesss")
                List_employe = Employes.objects.filter(fonction = type_depense)
                for emp in List_employe:
                    facture_emp = Facture.objects.filter(employe = emp)
                    for f_emp in facture_emp :
                        total_dep = total_dep+ f_emp.tarif

            else :
                prixsortie = Prixsortie.objects.filter(raison_payement=type_depense)
                
                for list in prixsortie :
                    total_dep = total_dep + list.prix_sortie
        context['total_dep'] = total_dep
        print('total_dep', context['total_dep'])
        context ['value'] =True  

          
        
        
        context['liste_depenses'] = prixsortie
        context['liste_depenses_rceherche'] = Depense.objects.all().values()
        return render(request, 'liste-depense.html', context)

    
    return render(request, 'liste-depense.html', context)
@login_required(login_url="/login/")
def ajouter_facture_depense(request):
    context = {}
    context['liste_depense'] = Depense.objects.all()
    

    return render(request, 'ajouter-facture-depense.html', context)

@login_required(login_url="/login/")
def valider_ajouter_depense(request):
    if request.method == "POST":
        type_depense = request.POST.get('depense')
        prix = decimal.Decimal(request.POST.get('prix'))
        prixsortie =Prixsortie(prix_sortie = prix ,raison_payement = type_depense)
        prixsortie.save(force_insert=True)
        messages.success(request, "depense a été bien enregistré") 

        
    return redirect('ajouter_facture_depense')    
@login_required(login_url="/login/")
def ajouter_achats(request) :
    if request.method =="POST" :
        prix = request.POST.get('prix')
        article = request.POST.get('article []')
        date = request.POST.get('date')

        achat = Prixsortie(prix_sortie=prix )
        achat.save(force_insert=True)

        if article : 
            for i in range(len(article)):
                obj_supplement =Stock.objects.get(id=article[i])
                if(True):
                    achat.article.add((obj_supplement))
        #Prixsortie.objects.get(id=achat).delete()
        messages.info(request, 'Achat a été bien crée')            
        redirect('liste_achats')
    return render(request, 'achats.html')
@login_required(login_url="/login/")
def ajouter_liste_achats(request) :
    context ={}
    context['segment'] = 'stock'
    context['liste_depense'] = Depense.objects.all().values().order_by("created_at").reverse()
    list = []
    list_none_article = Prixsortie.objects.filter(article = None).order_by("created_at").reverse()
    for i in list_none_article :
        list.append(i.id)
    list_achat = Prixsortie.objects.exclude(id__in=list)
    context['liste_achat'] = list_achat

    if request.method =="POST" :
        context['besoin_id'] = request.POST.get('besoin')
        context['besoin_article'] = request.POST.get('article')
        context['note'] = request.POST.get('note')
    
    return render(request, 'ajouter-achats.html' , context)
@login_required(login_url="/login/")
def ajouter_achats_article(request) :

    if request.method =="POST" :
        depense = request.POST.get('depense')  
        prix =  request.POST.get('prix')
        date =  request.POST.get('date')
        article = request.POST.get('article')
        print("this is article " , article)

        # list_article = Stock.objects.all()
        # value = False
        # for art in list_article :
        #      if art.article == article :
        #          achat = Prixsortie(prix_sortie =prix , raison_payement = depense ,date= date )
        #          achat.save(force_insert=True)
        #          achat.article.add(art)
        #          value = True

        # if value == False :
        # article = Stock(article = article)
        # article.save(force_insert=True)
        achat = Prixsortie(prix_sortie = prix , raison_payement = depense ,date = date ,article = article)
        achat.save(force_insert=True)
        # achat.article.add(article)

    return redirect('liste_stock')
@login_required(login_url="/login/")
def supprimer_achats(request):
    
    if request.method =="POST":
        achat = request.POST.get("id")
        
        Prixsortie.objects.get(id=achat).delete()
        messages.info(request, 'Achat a été bien supprimer')
            
       
    
    return redirect('ajouter_liste_achats')
@login_required(login_url="/login/")
def modifier_achats(request):
    context = {}
    if request.method =="POST":
        id_achat = request.POST.get("id")
        achat = Prixsortie.objects.get(id= id_achat) 
        context['achat'] = achat
        context['liste_depense'] = Depense.objects.all().values().order_by("created_at").reverse()
        

    return render(request, 'modifier-achats.html',context)
@login_required(login_url="/login/")
def valider_modifier_achats(request) :
    
    if request.method =="POST":
        depense = request.POST.get('depense')  
        prix =  request.POST.get('prix')
        date =  request.POST.get('date')
        article = request.POST.get('article')
        id_achat =request.POST.get('id')
        # achat =Prixsortie.objects.get(id =id_achat)
        # list_article = Stock.objects.all()
        # achat.article.clear()
        #article_pre = achat.article.all()

        # value = False
        # for art in list_article :
        #      if art.article == article :
        #          if date :
        #            Prixsortie.objects.filter(id = id_achat).update(date = date)
        #          Prixsortie.objects.filter(id = id_achat).update(prix_sortie = prix)
        #          achat.article.add(art)
        #          value = True
               
        # if value == False :
        # article = Stock(article = article)
        # article.save(force_insert=True)
        if date :
                Prixsortie.objects.filter(id = id_achat).update(date = date)
        Prixsortie.objects.filter(id = id_achat).update(prix_sortie = prix)
        Prixsortie.objects.filter(id = id_achat).update(article = article)
        Prixsortie.objects.filter(id = id_achat).update(raison_payement = depense)

        # achat.article.add(article)
        
        
        messages.info(request, 'Achat a été bien modifie')
    
    
    return redirect('ajouter_liste_achats')
@login_required(login_url="/login/")
def liste_achats(request) :
    context ={}
    context['segment'] = 'stock'
    context['liste_depense'] = Depense.objects.all().values().order_by("created_at").reverse()
    # context['liste_achat'] = Achat.objects.all().order_by("created_at").reverse()
    
    if request.method =="POST" :
        context['besoin_id'] = request.POST.get('besoin')
        context['besoin_article'] = request.POST.get('article')
        
        
    return render(request, 'achats.html' , context)

@login_required(login_url="/login/")    
def ajouter_achats_besoin(request) :
    if request.method =="POST" :
        depense = request.POST.get('depense')  
        prix =  request.POST.get('prix')
        date =  request.POST.get('date')
        besoin_id = request.POST.get('besoin_id')
        article = request.POST.get('article')
    
        Besoin.objects.get(id=besoin_id).delete()
        # list_article = Stock.objects.all()

        # value = False
        # for art in list_article :
        #      if art.article == article :
        #          achat = Prixsortie(date=date, prix_sortie=prix , raison_payement = depense)
        #          achat.save(force_insert=True)
        #          achat.article.add(art)            
        #          value = True

        # if value == False :
        # article = Stock (article = article)
        # article.save(force_insert=True)            
        achat = Prixsortie(date=date, prix_sortie=prix , raison_payement = depense , article =article)
        achat.save(force_insert=True)
        # achat.article.add(article)
        
        
        messages.info(request, 'achat de besoin a été bien crée')            

    return redirect('liste_besoin')
@login_required(login_url="/login/")
def liste_stock(request):
    context ={}
    context['segment'] = 'stock'
    list = []
    list_none_article = Prixsortie.objects.filter(article = None).order_by("created_at").reverse()
    for i in list_none_article :
        list.append(i.id)
    list_achat = Prixsortie.objects.exclude(id__in=list)

    context['liste_stock'] = list_achat

    return render(request, 'cuisine.html',context)
@login_required(login_url="/login/")    
def modifier_depense_prix(request) :
    context = {}
    if request.method =="POST":
        id_achat = request.POST.get("id")
        depense = Prixsortie.objects.get(id= id_achat) 
        context['depense'] = depense
        context['liste_depense'] = Depense.objects.all().values().order_by("created_at").reverse()
        

    return render(request, 'modifier-depense-prix.html',context)
@login_required(login_url="/login/")
def valider_modifier_depense(request) :
    if request.method =="POST":
        depense = request.POST.get('depense')  
        prix =  request.POST.get('prix')
        id_achat =request.POST.get('id')
        Prixsortie.objects.filter(id = id_achat).update(prix_sortie = prix)
        Prixsortie.objects.filter(id = id_achat).update(raison_payement = depense)

        # achat.article.add(article)
        
        
        messages.info(request, 'depense a été bien modifie')
    
    
    return redirect('liste_depenses')