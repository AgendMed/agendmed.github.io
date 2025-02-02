from django.contrib import admin
from .models import UnidadeSaude
from Profissional.models import ProfissionalSaude

class ProfissionalInline(admin.TabularInline):
    model = ProfissionalSaude
    extra = 0
    fields = ('usuario', 'especialidade', 'ativo')
    show_change_link = True

@admin.register(UnidadeSaude)
class UnidadeSaudeAdmin(admin.ModelAdmin):
    inlines = [ProfissionalInline]