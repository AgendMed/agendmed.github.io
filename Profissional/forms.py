from django import forms
from .models import ProfissionalSaude
from Unidade_Saude.models import UnidadeSaude

class ProfissionalSaudeForm(forms.ModelForm):
    nome = forms.CharField(max_length=150, required=True)
    
    unidade_saude = forms.ModelChoiceField(queryset=UnidadeSaude.objects.all(), required=True, label="Unidade de Saúde")
    
    class Meta:
        model = ProfissionalSaude
        fields = ['usuario', 'especialidade', 'unidade_saude']
