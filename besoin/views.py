from django.shortcuts import render ,redirect

# Create your views here.
from django.contrib import messages
from besoin.forms import BesoinForm,form_validation_error
from besoin.models import Besoin
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="/login/")
def ajouter_besoin(request):
    context = {}
    context['segment'] = 'besoin'
    if request.method =='POST':
        form = BesoinForm(request.POST or None)
        if form.is_valid():
            print("form is valid")
            form.save()
            messages.success(request, 'besoin a ete bien ajoute')
            return redirect('liste_besoin')
        else:
            print("form is not valid")
            messages.error(request,form_validation_error(form))

    return redirect('liste_besoin')
@login_required(login_url="/login/")
def liste_besoin(request):
    context ={}
    context['segment'] = 'stock'
    context['liste_besoin'] = Besoin.objects.all().values().order_by("created_at").reverse()
    return render(request, 'besoin-stock.html',context)
@login_required(login_url="/login/")
def supprimer_besoin(request):
    
    if request.method =="POST":
        besoin = request.POST.get("id")
        Besoin.objects.get(id=besoin).delete()
        
    return redirect('liste_besoin')

@login_required(login_url="/login/")
def modifier_besoin(request):
    context = {}
    if request.method =="POST":
        besoinid = request.POST.get("besoin")
        besoin = Besoin.objects.get(id= besoinid)
        context['besoin'] = besoin
        
         
    return render(request, 'modifier-besoin.html',context)
@login_required(login_url="/login/")
def valider_modifier_besoin(request) :
    
    if request.method =="POST":
        article = request.POST.get("article")
        note = request.POST.get("note")
        date = request.POST.get("date")
        id = request.POST.get("idbesoin")
      
        Besoin.objects.filter(id = id).update(article = article)
        Besoin.objects.filter(id = id).update(note = note)
        if date :
            Besoin.objects.filter(id = id).update(date = date)
            

        
        messages.info(request, 'besoin a été bien modifie')
    
    
    return redirect('liste_besoin')
