from django.contrib import admin, messages
from django.db.models import F
from .models import Consulta, Agendamento
from .forms import AgendamentoForm
from django.db import transaction


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('data', 'horario_formatado', 'profissional', 'unidade_saude', 'fichas_disponiveis')
    list_filter = ('data', 'unidade_saude', 'profissional')
    search_fields = ('profissional__usuario__nome_completo', 'unidade_saude__nome')
    filter_horizontal = ('lista_espera_prioritaria', 'lista_espera_comum')
    readonly_fields = ('horario_formatado',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('unidade_saude', 'profissional', 'data', 'horario_inicio', 'horario_fim')
        }),
        ('Controle de Vagas', {
            'fields': ('qtd_fichas_prioritarias', 'qtd_fichas_normais')
        }),
        ('Listas de Espera', {
            'fields': ('lista_espera_prioritaria', 'lista_espera_comum')
        }),
    )

    def fichas_disponiveis(self, obj):
        return f"🟠 {obj.qtd_fichas_prioritarias} | 🔵 {obj.qtd_fichas_normais}"
    fichas_disponiveis.short_description = 'Fichas Disponíveis'

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    form = AgendamentoForm
    list_display = ('consulta', 'paciente', 'data_agendamento', 'status_prioritario')
    list_filter = ('consulta__data', 'paciente__status')
    search_fields = ('paciente__usuario__nome_completo', 'consulta__profissional__usuario__nome_completo')
    raw_id_fields = ('paciente',)
    readonly_fields = ('data_agendamento',)

    @admin.display(boolean=True, description='Prioritário')
    def status_prioritario(self, obj):
        return obj.paciente.status == 'prioritario'

    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                if not change:
                    consulta = obj.consulta
                    paciente = obj.paciente

                    if paciente.status == 'prioritario':
                        Consulta.objects.filter(pk=consulta.pk, qtd_fichas_prioritarias__gt=0).update(
                            qtd_fichas_prioritarias=F('qtd_fichas_prioritarias') - 1
                        )
                    else:
                        Consulta.objects.filter(pk=consulta.pk, qtd_fichas_normais__gt=0).update(
                            qtd_fichas_normais=F('qtd_fichas_normais') - 1
                        )

                    consulta.refresh_from_db()
                    if (paciente.status == 'prioritario' and consulta.qtd_fichas_prioritarias < 0) or \
                       (paciente.status == 'comum' and consulta.qtd_fichas_normais < 0):
                        raise ValueError("Ficha não disponível!")

                super().save_model(request, obj, form, change)
                
        except Exception as e:
            messages.error(request, f"Erro ao agendar: {str(e)}")