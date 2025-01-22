from django.db import models
from django.conf import settings
from Unidade_Saude.models import UnidadeSaude


class ProfissionalSaude(models.Model):
    usuario = models.OneToOneField(
        settings.A,
        on_delete=models.CASCADE,
        related_name='profissional_saude'
    )
    especialidade = models.CharField(max_length=50)
    unidade_saude = models.ForeignKey(
        UnidadeSaude,
        on_delete=models.CASCADE,
        related_name='profissionais'
    )

    def __str__(self):
        return f"{self.usuario.nomeCompleto} - {self.especialidade}"
