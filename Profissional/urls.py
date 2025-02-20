from django.urls import path

from especialidades.views import listar_especialidades
from . import views
from .views import editar_perfil_profissional, perfil_profissional
from .views import filtrar_profissionais


app_name = 'profissional'


urlpatterns = [
    path('filtrar-profissionais/', filtrar_profissionais, name='filtrar_profissionais'),
    path('cadastro_profissional', views.cadastro_profissional, name='cadastro_profissional'),
    # path('profissional_home', views.profissional_home, name='profissional_home'),
    path('inicio/', views.pagina_inicial, name='paginainicial'),
    # path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('escolha-consulta/', listar_especialidades, name='listar_especialidades'),
    path('editar_perfil_profissional/', editar_perfil_profissional, name='editar_perfil_profissional'),
    path('perfil_profissional/', perfil_profissional, name='perfil_profissional'),
]
