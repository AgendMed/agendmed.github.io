from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['unidade_saude', 'profissional', 'data', 'horario', 'qtd_fichas_prioritarias', 'qtd_fichas_normais']

    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Adiciona o tipo 'date'

    def clean(self):
        cleaned_data = super().clean()
        unidade_saude = cleaned_data.get('unidade_saude')
        profissional = cleaned_data.get('profissional')
        qtd_prioritarias = cleaned_data.get('qtd_fichas_prioritarias', 0)
        qtd_normais = cleaned_data.get('qtd_fichas_normais', 0)

        # Valida se o profissional está vinculado à unidade de saúde
        if profissional and unidade_saude and profissional.unidade_saude != unidade_saude:
            self.add_error('profissional', "O profissional não está vinculado à unidade de saúde selecionada.")

        # Valida se há pelo menos uma ficha (normal ou prioritária)
        if qtd_prioritarias + qtd_normais <= 0:
            self.add_error(None, "A consulta deve ter pelo menos uma ficha disponível (normal ou prioritária).")

        return cleaned_data
