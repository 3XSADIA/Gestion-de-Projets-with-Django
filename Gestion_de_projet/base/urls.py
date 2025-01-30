from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.loginPage,name="login"),
    path('logout',views.logoutUser,name="logout"),
    path('register',views.registerUser,name="register"),

    path('',views.home,name="home"),
    path('tache_page/<str:pk>/',views.tache_page,name="tache"),
    path('projet_page/<str:pk>/',views.projet_page,name="projet"),
    path('create-tache/',views.createTache,name="create-tache"),
    path('create-projet/',views.createProjet,name="create-projet"),
    path('update-Tache/<str:pk>/',views.updateTache,name="update-Tache"),
    path('update-Projet/<str:pk>/',views.updateProjet,name="update-Projet"),
    path('delete-Tache/<str:pk>/',views.deleteTache,name="delete-Tache"),
    path('delete-Projet/<str:pk>/',views.deleteProjet,name="delete-Projet"),
    path('user-Profile/<str:pk>/',views.userProfile,name="user-Profile"),
    path('project/<str:pk>/export/',views.export_project_tasks, name='export_project_tasks'),



]
