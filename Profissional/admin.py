from django.contrib import admin
from .models import ProfissionalSaude

@admin.register(ProfissionalSaude)
class ProfissionalSaudeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidade', 'unidade_saude', 'ativo')
    list_filter = ('especialidade', 'unidade_saude')
    search_fields = ('usuario__nome_completo', 'especialidade__nome')
    raw_id_fields = ('usuario',)
    list_editable = ('ativo',)
    list_per_page = 20

    fieldsets = (
        ('Dados Principais', {
            'fields': ('usuario', 'especialidade', 'unidade_saude')
        }),
        ('Status', {
            'fields': ('ativo',),
            'classes': ('collapse',)
        }),
    )   