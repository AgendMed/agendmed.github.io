from django.urls import path

from especialidades.views import listar_especialidades
from . import views
from .views import acompanha_domicilio, atualizar_status_paciente, editar_paciente, editar_perfil_profissional, lista_pacientes_unidade, perfil_profissional, requisicoes_pendentes
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
    path('pacientes-agendados/', lista_pacientes_unidade, name='lista_pacientes_unidade'),
    path('editar-paciente/<int:paciente_id>/', editar_paciente, name='editar_paciente'),
    path('agendar/<int:consulta_id>/', views.agendar_consulta_paciente, name='agendar_consulta'),
    path('requisicoes_pendentes/', requisicoes_pendentes, name='requisicoes_pendentes'),
    path('atualizar-status/<int:paciente_id>/', atualizar_status_paciente, name='atualizar_status_paciente'),
    path('acompanha-domicilio/', acompanha_domicilio, name='acompanha_domicilio'),



]
