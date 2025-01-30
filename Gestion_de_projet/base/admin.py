from django.contrib import admin

# Register your models here.
from .models import tache,Projet

admin.site.register(tache)
admin.site.register(Projet)

