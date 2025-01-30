from django.shortcuts import render,redirect
from .models import tache,Projet
from .forms import TacheForm,ProjetForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.core.serializers.json import DjangoJSONEncoder
import json
def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"Utilisateur n'existe pas")
            
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"username ou password incorrectes")
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form=UserCreationForm()
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"an error occured during registration.")
    return render(request,"base/login_register.html",{"form":form})
def home(request):
    user = request.user  # Récupère l'utilisateur connecté
    q = request.GET.get('q', '')  # Récupère la valeur de 'q' ou une chaîne vide si 'q' n'existe pas
    # Si l'utilisateur est connecté, filtrer les tâches et projets en fonction de l'utilisateur
    if user.is_authenticated:
        taches = tache.objects.filter(
            Q(projet__utilisateur=user) |  # Tâches appartenant à des projets créés par l'utilisateur
            Q(utilisateur=user)  # Tâches où l'utilisateur est le réalisateur
        ).filter(
            Q(projet__nom__icontains=q) |  # Filtre supplémentaire pour la recherche
            Q(titre__icontains=q) |
            Q(description__icontains=q)
        ).distinct()  # Évite les doublons
        projets = Projet.objects.filter(utilisateur=user)  # Projets créés par l'utilisateur
    else:
        # Si l'utilisateur n'est pas connecté, afficher toutes les tâches et tous les projets
        taches = tache.objects.filter(
            Q(projet__nom__icontains=q) |  # Filtre pour la recherche
            Q(titre__icontains=q) |
            Q(description__icontains=q)
        ).distinct()
        projets = Projet.objects.all()  # Tous les projets
    projets_count = projets.count()
    taches_count = taches.count()
    # Vérifie si 'q' n'est pas vide avant de chercher un projet
    projet_obj = None
    if q:
        try:
            if user.is_authenticated:
                projet_obj = Projet.objects.get(nom=q, utilisateur=user)  # Projet appartenant à l'utilisateur
            else:
                projet_obj = Projet.objects.get(nom=q)  # Projet sans restriction d'utilisateur
        except Projet.DoesNotExist:
            # Si aucun projet ne correspond, on laisse projet_obj à None
            pass
    context = {'taches': taches,'projets': projets,'taches_count': taches_count,'projets_count': projets_count,'projet_obj': projet_obj}
    return render(request, 'base/home.html', context)
def tache_page(request,pk):
    tache_obj=tache.objects.get(id=pk)
    context={'tache':tache_obj}
    return render(request,'base/tache.html',context)

def projet_page(request,pk):
    projet_obj=Projet.objects.get(id=pk)
    context={'projet':projet_obj}
    return render(request,'base/projet.html',context)

@login_required(login_url='login')
def createTache(request):
    form=TacheForm()
    if request.method == 'POST':
        form=TacheForm(request.POST)
        if form.is_valid():
            tache = form.save(commit=False)
            projet=tache.projet 
            tache.save()            # Mettre à jour le statut du projet associé
            projet.update_statut()
            return redirect('home')
    context={"form":form}
    return render(request,'base/tache_form.html',context)

@login_required(login_url='login')
def updateTache(request,pk):
    tache_obj=tache.objects.get(id=pk)
    form=TacheForm(instance=tache_obj)
    if request.user != tache_obj.utilisateur:
        return HttpResponse(" Vous n'êtes pas autorisé !! ")
    if request.method == 'POST':
        form=TacheForm(request.POST,instance=tache_obj)
        if form.is_valid():
            form.save()
            # Mettre à jour le statut du projet associé
            tache_obj.projet.update_statut()
            return redirect('home')
            
    context={"form":form}
    return render(request,'base/tache_form.html',context)

@login_required(login_url='login')
def deleteTache(request,pk):
    projet = tache.projet
    tache_obj=tache.objects.get(id=pk)
    if request.method=='POST':
        tache_obj.delete()
        projet.update_statut()

        return redirect('home')
    return render(request,'base/delete.html',{'obj':tache_obj})


@login_required(login_url='login')
def createProjet(request):
    form = ProjetForm()
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            # Ne pas sauvegarder directement le formulaire
            projet = form.save(commit=False)
            # Associer l'utilisateur connecté au projet
            projet.utilisateur = request.user
            # Maintenant, sauvegarder le projet avec l'utilisateur associé
            projet.save()
            return redirect('home')
    
    context = {"form": form}
    return render(request, 'base/projet_form.html', context)
@login_required(login_url='login')
def updateProjet(request,pk):
    projet_obj=Projet.objects.get(id=pk)
    form=ProjetForm(instance=projet_obj)
    if request.user != projet_obj.utilisateur:
        return HttpResponse(" Vous n'êtes pas autorisé !! ")
    if request.method == 'POST':
        form=ProjetForm(request.POST,instance=projet_obj)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={"form":form}
    return render(request,'base/projet_form.html',context)

@login_required(login_url='login')
def deleteProjet(request,pk):
    projet_obj=Projet.objects.get(id=pk)
    if request.user != projet_obj.utilisateur:
       return HttpResponse(" Vous n'êtes pas autorisé !! ")
    if request.method=='POST':
        projet_obj.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':projet_obj})


def userProfile(request,pk):
    user=User.objects.get(id=pk)
    projets_count =Projet.objects.filter(utilisateur=user).count()
    taches_count = tache.objects.filter(utilisateur=user).count()
    context={"user":user,"projets_count":projets_count,"taches_count":taches_count}
    return render(request,'base/profile.html',context)



def export_project_tasks(request, pk):
    # Récupérer le projet et ses tâches
    project = Projet.objects.get(id=pk)
    tasks = tache.objects.filter(projet=project)

    # Formater les données en JSON
    data = {
        "project_name": project.nom,
        "taches": list(tasks.values('titre', 'description', 'statut', 'utilisateur', 'created'))
    }

    # Créer une réponse HTTP avec le fichier JSON
    response = HttpResponse(
        json.dumps(data, indent=4, cls=DjangoJSONEncoder),  # Utiliser DjangoJSONEncoder
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="projet_{pk}_tasks.json"'
    return response