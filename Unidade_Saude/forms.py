from django import forms
from .models import UnidadeSaude

class UnidadeSaudeForm(forms.ModelForm):
    nome = forms.CharField(max_length=100, required=True, label="Nome da Unidade")
    endereco = forms.CharField(max_length=200, required=True, label="Endereço")
    telefone = forms.CharField(max_length=15, required=False, label="Telefone")
    email = forms.EmailField(required=True, label="E-mail")

    class Meta:
        model = UnidadeSaude
        fields = ['nome', 'endereco', 'telefone', 'email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        # verificar se o e-mail já existe
        if email and UnidadeSaude.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe uma unidade de saúde cadastrada com este e-mail.')

        return cleaned_data

    def save(self, commit=True):
        unidade_saude = super().save(commit=False)

        if commit:
            unidade_saude.save()

        return unidade_saude

