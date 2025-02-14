from django import forms
from django.contrib.auth import get_user_model
from Profissional.models import ProfissionalSaude
from django.core.exceptions import ValidationError
from .models import ProfissionalSaude
from Unidade_Saude.models import UnidadeSaude
from especialidades.models import Especialidade
import requests
from users.models import Usuario  # Certifique-se de que o caminho está correto

class ProfissionalSaudeForm(forms.ModelForm):
    senha_atual = forms.CharField(widget=forms.PasswordInput, required=False)
    nova_senha = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = ProfissionalSaude
        fields = ['especialidade', 'unidade_saude']  # Apenas campos do modelo ProfissionalSaude

    def clean(self):
        cleaned_data = super().clean()
        senha_atual = cleaned_data.get("senha_atual")
        nova_senha = cleaned_data.get("confirmar_senha")

        if senha_atual:
            if not self.instance.usuario.check_password(senha_atual):  # Acessa o usuário associado
                raise ValidationError("A senha atual está incorreta.")

        if nova_senha and len(nova_senha) < 6:
            raise ValidationError("A nova senha deve ter pelo menos 6 caracteres.")

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
    

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome_completo', 'cpf', 'telefone', 'bairro', 'rua', 'complemento', 'numerocasa', 'data_nascimento', 'email']