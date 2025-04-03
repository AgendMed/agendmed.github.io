from django.urls import path
from .views import cadastrar_campanha, editar_campanha, lista_campanhas_gerais, listar_campanhas, deletar_campanha

app_name = 'Campanha'

urlpatterns = [
    path('cadastrar/', cadastrar_campanha, name='cad_Campanha'),
    path('listar/', listar_campanhas, name='listar_campanhas'),
    path('deletar/<int:campanha_id>/', deletar_campanha, name='deletar_campanha'),
    path('editar/<int:campanha_id>/', editar_campanha, name='editar_campanha'),
     path('campanhas/', lista_campanhas_gerais, name='lista_campanhas_gerais'),
]
