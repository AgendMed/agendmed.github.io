from django.urls import path

from especialidades.views import listar_especialidades
from . import views

app_name = 'profissional'


urlpatterns = [
    path('', views.cadastro_profissional, name='cadastro_profissional'),
    path('inicio/', views.pagina_inicial, name='paginainicial'),
    # path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('escolha-consulta/', listar_especialidades, name='listar_especialidades'),

]
