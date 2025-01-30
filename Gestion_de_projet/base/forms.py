from django.forms import ModelForm
from .models import tache,Projet

class TacheForm(ModelForm):
    class Meta:
        model=tache
        fields='__all__'
    
class ProjetForm(ModelForm):
     class Meta:
        model=Projet
        fields='__all__'