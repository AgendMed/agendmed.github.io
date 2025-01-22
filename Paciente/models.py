from django.db import models
<<<<<<< HEAD
from django.core.validators import MinLengthValidator

class Paciente(models.Model):
    CONDMEDICA_CHOICES = [
        ('nenhuma', 'Não possui condição'),
        ('gravidez', 'Gravidez (Gestante)'),
        ('idoso', 'Idoso (60 anos ou mais)'),
        ('doencas_cronicas', 'Doenças Crônicas Graves'),
        ('urgencia', 'Urgências e Emergências'),
        ('deficiencia', 'Deficiências Físicas ou Mentais'),
        ('imunossupresso', 'Pacientes Imunossuprimidos'),
        ('doencas_infectocontagiosas', 'Doenças Infectocontagiosas'),
    ]

    nome_completo = models.CharField(max_length=40)
    cartao_saude = models.IntegerField(unique=True)
    cpf = models.CharField(
        max_length=14,
        validators=[MinLengthValidator(11)],
        verbose_name="CPF",
        unique=True
    )
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    telefone = models.CharField(max_length=15)
    bairro = models.CharField(max_length=25)
    rua = models.CharField(max_length=45)
    num_casa = models.IntegerField()
    complemento = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    senha = models.CharField(max_length=30)
    condicao_prioritaria = models.CharField(
        max_length=50, 
        choices=CONDMEDICA_CHOICES, 
        default='nenhuma',
        null=True,  # Tornando esse campo opcional
        blank=True  # Tornando esse campo opcional
    )
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)

    campanhas = models.ManyToManyField('Campanha.Campanha', blank=True)

    def __str__(self):
        return self.cpf
=======
from users.models import Usuario


class Paciente(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cartao_saude = models.IntegerField(unique=True)
    condicao_prioritaria = models.CharField(
        max_length=50,
        choices=[
            ('nenhuma', 'Não possui condição'),
            ('gravidez', 'Gravidez (Gestante)'),
            ('idoso', 'Idoso (60 anos ou mais)'),
            ('doencas_cronicas', 'Doenças Crônicas Graves'),
            ('urgencia', 'Urgências e Emergências'),
            ('deficiencia', 'Deficiências Físicas ou Mentais'),
            ('imunossupresso', 'Pacientes Imunossuprimidos'),
            ('doencas_infectocontagiosas', 'Doenças Infectocontagiosas'),
        ],
        default='nenhuma',
        null=True,
        blank=True
    )
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)

    def __str__(self):
        return self.usuario.nome_completo
>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54
