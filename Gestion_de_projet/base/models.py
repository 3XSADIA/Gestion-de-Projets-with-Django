from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Projet(models.Model):
     # Choix pour le statut
    STATUS_CHOICES = [
        ('en cours', 'En cours'),
        ('terminé', 'Terminé'),
    ]
    utilisateur=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    nom=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
      # Ajout du champ statut
    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='en cours',  # Statut par défaut
    )
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=   ['-updated','-created']
    def __str__(self):
        return self.nom
     # Méthode pour mettre à jour le statut du projet
    def update_statut(self):
        # Récupérer toutes les tâches associées à ce projet
        taches = self.tache_set.all() 
        # Si toutes les tâches sont terminées, le projet est terminé
        if taches.count() > 0 and all(tache.statut == 'terminé' for tache in taches):
            self.statut = 'terminé'
        else:
            self.statut = 'en cours'
        # Sauvegarder le projet
        self.save()



class tache(models.Model):
     # Choix pour le statut
    STATUS_CHOICES = [
        ('à faire', 'À faire'),
        ('en cours', 'En cours'),
        ('terminé', 'Terminé'),
    ]
    utilisateur=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    projet=models.ForeignKey(Projet,on_delete=models.CASCADE,null=True)
    titre=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
     # Ajout du champ statut
    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='à faire',  # Statut par défaut
    )
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=   ['-updated','-created']
    def __str__(self):
        return self.titre
