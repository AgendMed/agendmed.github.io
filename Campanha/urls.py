from django.urls import path
from .views import cadastrar_campanha, listar_campanhas, deletar_campanha

app_name = 'Campanha'

urlpatterns = [
    path('cadastrar/', cadastrar_campanha, name='cad_Campanha'),
    path('listar/', listar_campanhas, name='listar_campanhas'),
    path('deletar/<int:campanha_id>/', deletar_campanha, name='deletar_campanha'),
]
