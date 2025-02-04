from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_consulta, name='cadastrar_consulta'),
    path('agendar/', views.agendar_consulta, name='agendar_consulta'),
    path('listar/', views.listar_consultas, name='listar_consultas'),


]
