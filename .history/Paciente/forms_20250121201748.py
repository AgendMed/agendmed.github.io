from django import forms
from .models import Usuario, Paciente


class CadastroPacienteForm(forms.ModelForm):
    # Campos do modelo Usuario
    nome_completo = forms.CharField(max_length=150, required=True)
    cpf = forms.CharField(max_length=14, required=True)
    telefone = forms.CharField(max_length=15, required=False)
    endereco = forms.CharField(max_length=255, required=False)


    dataNascimento = forms.DateField()
    Bairro = forms.TextField(max_length=255, )
    Rua = forms.TextField(max_length=255, )
    complemento = forms.CharField(max_length=255, )
    NumeroCasa = forms.CharField(max_length=30, )

    # Campos do modelo Paciente
    cartao_saude = forms.CharField(max_length=15, required=True)
    data_nascimento = forms.DateField(required=True)
    condicao_prioritaria = forms.ChoiceField(choices=Paciente._meta.get_field('condicao_prioritaria').choices, required=False)
    comprovante = forms.FileField(required=False)


    class Meta:
        model = Paciente
        fields = ['cartao_saude', 'data_nascimento', 'condicao_prioritaria', 'comprovante']

    def save(self, commit=True):
        # Salva o usuário primeiro
        usuario_data = {
            'username': self.cleaned_data['cpf'],  # Usando o CPF como username por exemplo
            'nome_completo': self.cleaned_data['nome_completo'],
            'cpf': self.cleaned_data['cpf'],
            'telefone': self.cleaned_data['telefone'],
            'endereco': self.cleaned_data['endereco'],
        }

        usuario = Usuario.objects.create(**usuario_data)

        # Cria o paciente associado ao usuário
        paciente_data = {
            'usuario': usuario,
            'cartao_saude': self.cleaned_data['cartao_saude'],
            'data_nascimento': self.cleaned_data['data_nascimento'],
            'condicao_prioritaria': self.cleaned_data['condicao_prioritaria'],
            'comprovante': self.cleaned_data['comprovante'],
        }

        paciente = Paciente.objects.create(**paciente_data)

        return paciente




