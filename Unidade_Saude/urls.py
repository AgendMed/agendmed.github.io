from django.urls import path
from . import views

app_name = 'UnidadeSaude'

urlpatterns = [
    path('cadastro/', views.cadastro_unidade_saude, name='cadastro_unidade_saude'),  # URL para o cadastro
    path('sucesso/', views.sucesso, name='sucesso'),  # URL para a página de sucesso
    path('unidade/<int:pk>/', views.detalhe_unidade_saude, name='detalhe_unidade'),
    path('editar/<int:pk>/', views.editar_unidade_saude, name='editar_unidade_saude'),



]
