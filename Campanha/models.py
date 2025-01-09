from django.db import models

class Campanha(models.Model):
    titulo = models.CharField(max_length=50)
    subtitulo = models.CharField(max_length=80)
    descricao = models.TextField()
    dataInicial = models.DateField()
    dataFinal = models.DateField()
    imagem = models.ImageField(upload_to='imagens/', null=True, blank=True)

    def __str__(self):
        return self.titulo
