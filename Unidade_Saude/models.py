from django.db import models

class UnidadeSaude(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome
