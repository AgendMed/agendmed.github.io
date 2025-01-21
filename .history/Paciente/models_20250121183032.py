from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

from users.models import Usuario


class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=1)
    cartao_saude = models.IntegerField(unique=True)
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
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
        return self.usuario.nomeCompleto
