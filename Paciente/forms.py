from django import forms
from .models import Usuario, Paciente
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group, Permission


class CadastroPacienteForm(forms.ModelForm):
    # Campos do modelo Usuario
    nome_completo = forms.CharField(max_length=150, required=True)
    cpf = forms.CharField(max_length=14, required=True)
    telefone = forms.CharField(max_length=15, required=False)
    bairro = forms.CharField(max_length=255, required=False)
    rua = forms.CharField(max_length=255, required=False)
    complemento = forms.CharField(max_length=255, required=False)
    numerocasa = forms.CharField(max_length=30, required=False)
    data_nascimento = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(widget=forms.PasswordInput, required=True)

    # Campos do modelo Paciente
    cartao_saude = forms.CharField(max_length=15, required=True)
    condicao_prioritaria = forms.ChoiceField(
        choices=Paciente._meta.get_field('condicao_prioritaria').choices, required=False)
    comprovante = forms.FileField(required=False)

    class Meta:
        model = Paciente
        fields = ['cartao_saude', 'condicao_prioritaria', 'comprovante']

    def clean(self):
        cleaned_data = super().clean()
        nome_completo = cleaned_data.get('nome_completo')
        
        if not nome_completo:
            raise forms.ValidationError('O campo nome completo é obrigatório.')

        # Validação adicional para CPF e E-mail
        if not cleaned_data.get('cpf'):
            raise forms.ValidationError('O CPF é obrigatório.')

        if not cleaned_data.get('email'):
            raise forms.ValidationError('O E-mail é obrigatório.')

        # Validação do comprovante, se presente
        comprovante = cleaned_data.get('comprovante')
        if comprovante and not comprovante.name.endswith(('.pdf', '.jpg', '.png')):
            raise ValidationError('O arquivo de comprovante deve ser PDF, JPG ou PNG.')

        return cleaned_data

    def save(self, commit=True):
        # Criação do usuário de forma segura
        usuario = Usuario.objects.create_user(
            username=self.cleaned_data['cpf'],  # Usando o CPF como username
            nome_completo=self.cleaned_data['nome_completo'],
            cpf=self.cleaned_data['cpf'],
            telefone=self.cleaned_data['telefone'],
            bairro=self.cleaned_data['bairro'],
            rua=self.cleaned_data['rua'],
            complemento=self.cleaned_data['complemento'],
            numerocasa=self.cleaned_data['numerocasa'],
            data_nascimento=self.cleaned_data['data_nascimento'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['senha']
        )

        # Criação do paciente associado ao usuário
        paciente_data = {
            'usuario': usuario,
            'cartao_saude': self.cleaned_data['cartao_saude'],
            'condicao_prioritaria': self.cleaned_data['condicao_prioritaria'],
            'comprovante': self.cleaned_data['comprovante'],
        }

        paciente = Paciente.objects.create(**paciente_data)

        # Adiciona o paciente ao grupo de Paciente, se existir
        grupo_paciente = Group.objects.get(name='Paciente')
        paciente.usuario.groups.add(grupo_paciente)

        return paciente
