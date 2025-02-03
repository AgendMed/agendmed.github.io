from django.db import models
from Unidade_Saude.models import UnidadeSaude

class Campanha(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=150, blank=True)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='campanhas/', null=True, blank=True)
    data_inicial = models.DateField()
    data_final = models.DateField()
    
    unidade_saude = models.ForeignKey(
    UnidadeSaude,
    on_delete=models.CASCADE,
    related_name='campanhas',
    null=True,
    blank=True
)

    def __str__(self):
        return self.titulo
