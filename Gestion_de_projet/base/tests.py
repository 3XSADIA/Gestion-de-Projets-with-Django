from django.test import TestCase
from .models import Projet, tache
from django.contrib.auth.models import User
from django.test import Client

class ProjetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.projet = Projet.objects.create(nom="Projet Test", utilisateur=self.user)
    def test_projet_creation(self):
        self.assertEqual(self.projet.nom, "Projet Test")
        self.assertEqual(self.projet.utilisateur.username, "testuser")

class TacheModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.projet = Projet.objects.create(nom="Projet Test", utilisateur=self.user)
        self.tache = tache.objects.create(
            titre="Tâche Test",
            description="Description de test",
            projet=self.projet,
            utilisateur=self.user)
    def test_tache_creation(self):
        self.assertEqual(self.tache.titre, "Tâche Test")
        self.assertEqual(self.tache.projet.nom, "Projet Test")

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.projet = Projet.objects.create(nom="Projet Test", utilisateur=self.user)
    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_login_view(self):
        # Test de la connexion réussie
        response = self.client.post('/login/', {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)  # Redirection après connexion
        # Vérifier que l'utilisateur est bien connecté
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_projet_creation_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create-projet/', {'nom': 'Nouveau Projet', 'utilisateur': self.user.id})
        self.assertEqual(response.status_code, 200)