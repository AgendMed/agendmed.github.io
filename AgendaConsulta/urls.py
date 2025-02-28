from django.urls import path
from . import views

app_name = "AgendaConsulta"

urlpatterns = [
    path('cadastrar/', views.cadastrar_consulta, name='cadastrar_consulta'),
    path('agendar-consulta/<int:consulta_id>/', views.agendar_consulta, name='agendar_consulta'), #para agendar consulta através do id da
    path('listar/', views.listar_consultas, name='listar_consultas'),
    path('cancelar/<int:consulta_id>/', views.cancelar_consulta, name='cancelar_consulta'),
    path('editar/<int:consulta_id>/', views.editar_consulta, name='editar_consulta'),
    path('listar_pacientes/<int:consulta_id>/', views.listar_pacientes_por_consulta, name='listar_pacientes_por_consulta'),
    path('alocar-paciente/<int:paciente_id>/', views.alocar_paciente, name='alocar_paciente'),
    path('cancelar-agendamento/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),



]