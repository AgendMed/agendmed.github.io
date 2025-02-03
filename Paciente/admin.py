from django.contrib import admin
from .models import Paciente
from django.utils import timezone

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'status', 'condicao_prioritaria', 'data_aprovacao', 'comprovante')
    list_filter = ('status', 'condicao_prioritaria')
    search_fields = ('usuario__nome_completo', 'cartao_saude')
    actions = ['aprovar_comprovante']

    def aprovar_comprovante(self, request, queryset):
        updated = queryset.filter(comprovante__isnull=False).update(
            status='prioritario',
            data_aprovacao=timezone.now()
        )
        self.message_user(request, f"{updated} pacientes aprovados como prioritários!")
    
    aprovar_comprovante.short_description = "Aprovar comprovantes selecionados"