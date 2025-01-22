from django.urls import path
from . import views

app_name = 'Paciente'

urlpatterns = [
    path('sucesso/', views.sucesso, name='sucesso'),
    path('cadastro/', views.cadastro_paciente, name='cadastro_paciente'),
    path('login/', views.login_view, name='login'),
<<<<<<< HEAD
]
=======
    path('index/', views.Index_view, name='index'),

]
>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54
