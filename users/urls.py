from django.urls import path
from . import views
from .views import listar_tabelas


app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('listar-tabelas/', listar_tabelas, name='listar_tabelas'),

]
