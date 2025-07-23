from django.urls import path

from Unidade_Saude.views import detalhe_unidade_saude
from . import views

app_name = 'Paciente'

urlpatterns = [
    path('sucesso/', views.sucesso, name='sucesso'),
    path('cadastro/', views.cadastro_paciente, name='cadastro_paciente'),
    path('index/', views.Index_view, name='index'),
    path('pagina/', views.pagina_paciente, name='pagina_paciente'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('logout/', views.logout_view, name='logout'),
    path('paciente_home/', views.paciente_home, name='paciente_home'),
    path('listar/', views.listar_consultas, name='listar_consultas'),
    path('notificacoes/', views.notificacoes, name='notificacoes'), #visualizar notificacoes na tela paciente
    path('marcar-como-lida/<int:notificacao_id>/', views.marcar_como_lida, name='marcar_como_lida'),
    path('minhas-consultas/', views.lista_minhas_consultas, name='lista_minhas_consultas'),
    path('cancelar-agendamento/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('paciente/<int:paciente_id>/localizacao/', views.ver_localizacao_paciente, name='ver_localizacao_paciente'),

]
