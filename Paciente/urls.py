from django.urls import path
from . import views

app_name = 'Paciente'

urlpatterns = [
    path('sucesso/', views.sucesso, name='sucesso'),
    path('cadastro/', views.cadastro_paciente, name='cadastro_paciente'),
    path('index/', views.Index_view, name='index'),
#    path('listar/', views.listar_consultas, name='listar_consultas'),
    path('agendar-consulta/<int:consulta_id>/', views.agendar_consulta, name='agendar_consulta'),

]
