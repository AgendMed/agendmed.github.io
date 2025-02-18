from django.urls import path

from especialidades.views import listar_especialidades
from . import views
from .views import editar_perfil_profissional, perfil_profissional

app_name = 'profissional'


urlpatterns = [
    path('cadastro_profissional', views.cadastro_profissional, name='cadastro_profissional'),
    # path('profissional_home', views.profissional_home, name='profissional_home'),
    path('inicio/', views.pagina_inicial, name='paginainicial'),
    # path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
<<<<<<< HEAD
<<<<<<< HEAD
    path('editar_perfil_profissional/', editar_perfil_profissional, name='editar_perfil_profissional'),
    path('perfil_profissional/', perfil_profissional, name='perfil_profissional'),
=======
    path('escolha-consulta/', listar_especialidades, name='listar_especialidades'),

>>>>>>> be4015d84aaa5e01bfc1932105eeb35a617fd044
=======
    path('escolha-consulta/', listar_especialidades, name='listar_especialidades'),

    path('editar_perfil_profissional/', editar_perfil_profissional, name='editar_perfil_profissional'),
    path('perfil_profissional/', perfil_profissional, name='perfil_profissional'),
>>>>>>> 393249b43ab7064a0eac261e684937738c6f6bad
]
