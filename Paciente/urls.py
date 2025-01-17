from django.urls import path
from . import views

app_name = 'Paciente'

urlpatterns = [
    path('sucesso/', views.sucesso, name='sucesso'),
    path('cadastro/', views.cadastro_paciente, name='cadastro_paciente'),
    path('login/', views.login_view, name='login'),

]
