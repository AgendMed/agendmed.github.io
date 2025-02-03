from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.pagina_admin, name='pagina_admin'),
    path('medico/', views.pagina_medico, name='pagina_medico'),
    path('paciente/', views.pagina_paciente, name='pagina_paciente'),
]
