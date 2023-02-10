from django.contrib import admin
from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.index, name='home'),
    path('cursos/', views.cursos, name="cursos"),        
    path('prematricula/', views.prematricula, name="prematricula"),

]