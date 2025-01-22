from django import forms
from .models import Paciente
from django.contrib.auth import get_user_model

User = get_user_model()

class PacienteForm(forms.ModelForm):
    nomeCompleto = forms.CharField(max_length=255)
    cpf = forms.CharField(max_length=14)
    telefone = forms.CharField(max_length=15)

    class Meta:
        model = Paciente
        fields = ['cartao_saude', 'data_nascimento', 'condicao_prioritaria', 'comprovante']

    def save(self, commit=True):
        paciente = super().save(commit=False)
        usuario = paciente.usuario

        usuario.nomeCompleto = self.cleaned_data['nomeCompleto']
        usuario.cpf = self.cleaned_data['cpf']
        usuario.telefone = self.cleaned_data['telefone']
        if commit:
            usuario.save()
            paciente.save()
        return paciente
