from django import forms
from django.core.exceptions import ValidationError
from .models import Consulta, Agendamento

class ConsultaForm(forms.ModelForm):
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Consulta
        fields = ['data', 'unidade_saude', 'profissional', 'horario_inicio', 'horario_fim', 
                 'qtd_fichas_prioritarias', 'qtd_fichas_normais']
        
    def clean(self):
        cleaned_data = super().clean()
        unidade = cleaned_data.get('unidade_saude')
        profissional = cleaned_data.get('profissional')
        
        if unidade and profissional and profissional.unidade_saude != unidade:
            self.add_error('profissional', "Profissional não pertence à unidade selecionada")
        
        if cleaned_data.get('qtd_fichas_prioritarias', 0) + cleaned_data.get('qtd_fichas_normais', 0) <= 0:
            self.add_error(None, "Deve haver pelo menos uma ficha disponível")

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        consulta = cleaned_data.get('consulta')
        tipo_ficha = cleaned_data.get('tipo_ficha')

        if consulta and tipo_ficha:
            if tipo_ficha == 'prioritario' and consulta.qtd_fichas_prioritarias < 1:
                raise ValidationError("Não há fichas prioritárias disponíveis.")
            elif tipo_ficha == 'comum' and consulta.qtd_fichas_normais < 1:
                raise ValidationError("Não há fichas normais disponíveis.")
          

#Modal para notificações
class CancelamentoConsultaForm(forms.Form):
    RAZOES_CANCELAMENTO = [
        ('medico_doente', 'Médico doente'),
        ('problemas_deslocamento', 'Problemas de deslocamento'),
        ('compromisso_profissional', 'Compromisso profissional urgente'),
        ('problemas_unidade', 'Problemas na unidade de saúde'),
        ('mudanca_agenda', 'Mudança de agenda'),
        ('licenca_medica', 'Licença médica ou afastamento temporário'),
        ('ausencia_nao_comunicada', 'Ausência programada não comunicada'),
        ('cancelamento_administrativo', 'Cancelamento administrativo'),
    ]

    razao = forms.ChoiceField(choices=RAZOES_CANCELAMENTO, label="Razão do Cancelamento")