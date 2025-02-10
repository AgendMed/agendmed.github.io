import os
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from AgendMed.settings import BASE_DIR
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paciente/', include('Paciente.urls')),
    path('unidade-saude/', include('Unidade_Saude.urls')),
    path('cadastro_profissional/', include('Profissional.urls')),
    path('especialidades/', include('especialidades.urls')),
    path('cadastrar/', include('AgendaConsulta.urls')),
    path('users/', include('users.urls', namespace='users')),
    
    
    # Servir o index.html diretamente
    re_path(r'^$', serve, {'path': 'index.html', 'document_root': BASE_DIR}),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


