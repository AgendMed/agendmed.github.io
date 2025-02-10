from django.urls import path
from . import views

app_name = 'profissional'


urlpatterns = [
    path('', views.cadastro_profissional, name='cadastro_profissional'),
    path('profissional_home', views.profissional_home, name='profissional_home'),
    path('inicio/', views.pagina_inicial, name='paginainicial'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]
