from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'nome_completo', 'cpf', 'is_staff')
    search_fields = ('username', 'nome_completo', 'cpf')
    list_filter = ('groups', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': (
            'nome_completo',
            'cpf',
            'data_nascimento',
            'telefone'
        )}),
        ('Endereço', {'fields': (
            'bairro',
            'rua',
            'complemento',
            'numerocasa'
        )}),
        ('Permissões', {'fields': (
            'groups',
            'user_permissions',
            'is_staff',
            'is_superuser'
        )}),
        ('Geolocalização', {'fields': (
            'latitude',
            'longitude'
        )}),
    )

admin.site.register(Usuario, UsuarioAdmin)