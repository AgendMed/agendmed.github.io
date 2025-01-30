from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar-especialidade/', views.cadastrar_especialidade, name='cadastrar_especialidade'),
    path('sucesso/', views.especialidade_sucesso, name='especialidade_sucesso'),
]
