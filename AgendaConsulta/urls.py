from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_consulta, name='cadastrar_consulta'),
]
