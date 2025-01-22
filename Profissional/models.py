from django.db import models
<<<<<<< HEAD
from Unidade_Saude.models import UnidadeSaude

class ProfissionalSaude(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=50)
    unidade_saude = models.ForeignKey(UnidadeSaude, on_delete=models.CASCADE, related_name='profissionais')

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"
=======
from django.conf import settings
from Unidade_Saude.models import UnidadeSaude
from users.models import Usuario


class ProfissionalSaude(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=2)
    especialidade = models.CharField(max_length=50)
    unidade_saude = models.ForeignKey(
        UnidadeSaude,
        on_delete=models.CASCADE,
        related_name='profissionais'
    )

    def __str__(self):
        return f"{self.usuario.nomeCompleto} - {self.especialidade}"
>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54
