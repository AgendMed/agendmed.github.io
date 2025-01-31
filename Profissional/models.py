from django.db import models
from Unidade_Saude.models import UnidadeSaude
from especialidades.models import Especialidade
from users.models import Usuario


class ProfissionalSaude(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=2)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)
    unidade_saude = models.ForeignKey(
        UnidadeSaude,
        on_delete=models.CASCADE,
        related_name='profissionais'
    )

    def __str__(self):
        return f"{self.usuario.nome_completo} - {self.especialidade}"
