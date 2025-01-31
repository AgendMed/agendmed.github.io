from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastro_profissional, name='cadastro_profissional'),
]
