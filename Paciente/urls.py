from django.urls import path
from . import views

app_name = 'Paciente'

urlpatterns = [
    path('sucesso/', views.sucesso, name='sucesso'),
    path('cadastro/', views.cadastro_paciente, name='cadastro_paciente'),
    path('login/', views.login_view, name='login'),
    path('home/', views.paciente_home, name='home'),
    path('index/', views.Index_view, name='index'),
    path('pagina/', views.pagina_paciente, name='pagina_paciente'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('logout/', views.logout_view, name='logout'),  # Atualizando para usar a nova função
]