from django.shortcuts import render ,redirect
from django.contrib import messages
from stock.forms import StockForm,form_validation_error
from stock.models import Stock
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="/login/")
def ajouter_article(request):
    context = {}
    context['segment'] = 'stock'
    if request.method =='POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            print("form is valid")
            form.save()
            messages.success(request, 'article a ete bien ajoute')
            return redirect('liste_stock')
        else:
            print("form is not valid")
            messages.error(request,form_validation_error(form))
    

    return render(request, 'besoin-stock.html',context)
@login_required(login_url="/login/")    
def liste_stock(request):
    context ={}
    context['segment'] = 'stock'
    context['liste_stock'] = Stock.objects.all().values().order_by("created_at").reverse()
    return render(request, 'cuisine.html',context)
@login_required(login_url="/login/")
def supprimer_stock(request):
    
    if request.method =="POST":
        stock = request.POST.get("id")
        
    
    Stock.objects.get(id=stock).delete()
    
    return redirect('liste_stock')
@login_required(login_url="/login/")
def modifier_stock(request):
    context = {}
    if request.method =="POST":
        stock = request.POST.get("id")
        stock = Stock.objects.get(id= stock)
        context['stock'] = stock
         
    
    
    return render(request, 'modifier-stock.html',context)
@login_required(login_url="/login/")    
def valider_modifier_stock(request) :
    
    if request.method =="POST":
        stock = request.POST.get("stock_id")
        article = request.POST.get("article")
        list_article = Stock.objects.all()
        for list in list_article :
            if list.article == article :
                messages.error(request,'nom d article existe déja')
                return redirect('liste_stock')


        Stock.objects.filter(id = stock).update(article = article)
        messages.info(request, 'stock a été bien modifie')
    
    
    return redirect('liste_stock')
