from django.db import models
from especialidades.models import Especialidade

class UnidadeSaude(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    especialidades = models.ManyToManyField(Especialidade, blank=True)

    def __str__(self):
        return self.nome