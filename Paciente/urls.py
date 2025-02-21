from django.urls import path
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
    


]
