from django.db.models.expressions import Value
from django.shortcuts import redirect, render
from django.contrib import messages
from achats.models import Achat
from stock.models import Stock
from depenses.models import Depense
from besoin.models import Besoin
from prixsortie.models import Prixsortie
from decimal import Decimal
from django.contrib.auth.decorators import login_required


# def liste_achats(request) :
#     context ={}
#     context['segment'] = 'stock'
#     context['liste_depense'] = Depense.objects.all().values().order_by("created_at").reverse()
#     context['liste_achat'] = Achat.objects.all().order_by("created_at").reverse()
    
#     if request.method =="POST" :
#         context['besoin_id'] = request.POST.get('besoin')
#         context['besoin_article'] = request.POST.get('article')
#         context['note'] = request.POST.get('note')
        
#     return render(request, 'achats.html' , context)
@login_required(login_url="/login/")
def ajouter_achats(request) :
    if request.method =="POST" :
        prix = request.POST.get('prix')
        article = request.POST.get('article []')
        date = request.POST.get('date')

        achat = Achat(date=date, prix=prix )
        achat.save(force_insert=True)

        if article : 
            for i in range(len(article)):
                obj_supplement =Stock.objects.get(id=article[i])
                if(True):
                    achat.article.add((obj_supplement))
        Achat.objects.get(id=achat).delete()
        messages.info(request, 'Achat a été bien crée')            
        redirect('liste_achats')
    return render(request, 'achats.html')

# def ajouter_achats_besoin(request) :
#     if request.method =="POST" :
#         depense = request.POST.get('depense')  
#         prix =  request.POST.get('prix')
#         date =  request.POST.get('date')
#         besoin_id = request.POST.get('besoin_id')
#         article = request.POST.get('article')
    
#         note = request.POST.get('note')
#         # q = Decimal(qt.replace(',','.'))
#         Besoin.objects.get(id=besoin_id).delete()
#         list_article = Stock.objects.all()

#         value = False
#         for art in list_article :
#              if art.article == article :
#                 #  qantite = q + art.qantite
#                 #  Stock.objects.filter(id = art.id).update(qantite = qantite)
#                  achat = Achat(date=date, prix=prix)
#                  achat.save(force_insert=True)
#                  achat.article.add(art)            
#                  value = True

#         if value == False :
#             article = Stock (article = article)
#             article.save(force_insert=True)
            
#             achat = Achat(date=date, prix=prix)
#             achat.save(force_insert=True)
#             achat.article.add(article)
        
#         prixsortie=Prixsortie(prix_sortie = prix , raison_payement = depense)
#         prixsortie.save(force_insert=True)
#         messages.info(request, 'besoin a été bien crée')            

#     return redirect('liste_besoin')

@login_required(login_url="/login/")
def valider_achats(request) :
    if request.method =="POST" :
        depense = request.POST.get('depense')
        prix = request.POST.get('prix')
        article = request.POST.get('article []')
        date = request.POST.get('date')

        achat = Achat(date=date, prix=prix )
        achat.save(force_insert=True)

        if article : 
            for i in range(len(article)):
                obj_supplement =Stock.objects.get(id=article[i])
                if(True):
                    achat.article.add((obj_supplement))
        messages.info(request, 'Achat a été bien crée')            

        redirect('liste_achats')
    return render(request, 'achats.html')

# def ajouter_liste_achats(request) :
#     context ={}
#     context['segment'] = 'stock'
#     context['liste_depense'] = Depense.objects.all().values().order_by("created_at").reverse()
#     context['liste_achat'] = Achat.objects.all().order_by("created_at").reverse()
    
#     return render(request, 'ajouter-achats.html' , context)

# def ajouter_achats_article(request) :

#     if request.method =="POST" :
#         depense = request.POST.get('depense')  
#         prix =  request.POST.get('prix')
#         date =  request.POST.get('date')
#         article = request.POST.get('article')
#         print("this is article " , article)
    
#         # qt = request.POST.get('qantite')
        
        
#         list_article = Stock.objects.all()

#         value = False
#         for art in list_article :
#              if art.article == article :
#                 # q = Decimal(qt.replace(',','.'))
#                 # qantite = q + art.qantite
#                 # Stock.objects.filter(id = art.id).update(qantite = qantite)
#                  achat = Achat(date=date, prix=prix)
#                  achat.save(force_insert=True)
#                  achat.article.add(art)
#                  value = True

#         if value == False :
#             article = Stock(article = article)
#             article.save(force_insert=True)
#             achat = Achat(date=date, prix=prix)
#             achat.save(force_insert=True)
#             achat.article.add(article)

#         prixsortie=Prixsortie(prix_sortie = prix , raison_payement = depense ,achat = achat)
#         prixsortie.save(force_insert=True)
#     return redirect('ajouter_liste_achats')

# def supprimer_achats(request):
    
#     if request.method =="POST":
#         achat = request.POST.get("id")
#         Achat.objects.get(id=achat).delete()
#         messages.info(request, 'Achat a été bien supprimer')
            
    
    
#     return redirect('ajouter_liste_achats')

# def modifier_achats(request):
#     context = {}
#     if request.method =="POST":
#         id_achat = request.POST.get("id")
#         achat = Achat.objects.get(id= id_achat)
#         prixsortie = Prixsortie.objects.get(achat =achat)
#         context['achat'] = achat
#         context['prixsortie'] = prixsortie
        
        

#     return render(request, 'modifier-achats.html',context)

# def valider_modifier_achats(request) :
    
#     if request.method =="POST":
#         depense = request.POST.get('depense')  
#         prix =  request.POST.get('prix')
#         date =  request.POST.get('date')
#         article = request.POST.get('article')
#         id_achat =request.POST.get('id')
#         achat =Achat.objects.get(id =id_achat)
#         list_article = Stock.objects.all()
#         achat.article.clear()
#         #article_pre = achat.article.all()

#         value = False
#         for art in list_article :
#              if art.article == article :
#                  if date :
#                    Achat.objects.filter(id = id_achat).update(date = date)
#                  Achat.objects.filter(id = id_achat).update(prix = prix)
#                  achat.article.add(art)
#                  value = True
               
#         if value == False :
#             article = Stock(article = article)
#             article.save(force_insert=True)
#             if date :
#                 Achat.objects.filter(id = id_achat).update(date = date)
#             Achat.objects.filter(id = id_achat).update(prix = prix)
#             achat.article.add(article)
        
#         Prixsortie.objects.filter(achat = achat).update(raison_payement = depense)
#         Prixsortie.objects.filter(achat = achat).update(prix_sortie = prix)

#         messages.info(request, 'Achat a été bien modifie')
    
    
#     return redirect('ajouter_liste_achats')
