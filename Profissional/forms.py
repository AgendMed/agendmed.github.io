from django import forms
from django.contrib.auth import get_user_model
from Profissional.models import ProfissionalSaude
from Unidade_Saude.models import UnidadeSaude
from especialidades.models import Especialidade
import requests
from django.core.exceptions import ValidationError

from django import forms
from .models import ProfissionalSaude
from Unidade_Saude.models import UnidadeSaude
from especialidades.models import Especialidade
from django.core.exceptions import ValidationError

from django import forms
from django.contrib.auth import get_user_model
from Profissional.models import ProfissionalSaude
from Unidade_Saude.models import UnidadeSaude
from especialidades.models import Especialidade
import requests
from django.core.exceptions import ValidationError

class ProfissionalSaudeForm(forms.ModelForm):
    nova_senha = forms.CharField(widget=forms.PasswordInput(), required=False, label="Nova Senha")
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(), required=False, label="Confirmar Nova Senha")

    class Meta:
        model = ProfissionalSaude
        fields = ['especialidade', 'unidade_saude']  # Apenas campos do modelo ProfissionalSaude

    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get("nova_senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if nova_senha and nova_senha != confirmar_senha:
            raise ValidationError("As senhas não coincidem.")

        return cleaned_data
    
    def save(self, commit=True):
        profissional = super().save(commit=False)
        usuario = profissional.usuario

        # Verifica se a nova senha foi fornecida
        nova_senha = self.cleaned_data.get('nova_senha')
        if nova_senha:
            usuario.set_password(nova_senha)
            usuario.save()

        if commit:
            profissional.save()

        return profissional
    
from django import forms
from users.models import Usuario  # Certifique-se de que o caminho está correto

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome_completo', 'cpf', 'telefone', 'bairro', 'rua', 'complemento', 'numerocasa', 'data_nascimento', 'email']