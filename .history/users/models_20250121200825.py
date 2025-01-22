from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Usuario(AbstractUser):
    nome_completo = models.CharField(max_length=150, null=False, default='Nome não informado')
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=30, blank=True, null=False, default='Telefone não informado')
    dataNascimento = models.DateField(null=False, blank=True, default='dataNascimento não informado')
    Bairro = models.TextField(max_length=255, blank=True, null=False, default='Endereço não informado')
    Rua = models.TextField(max_length=255, blank=True, null=False, default='Rua não informada')
    complemento = models.TextField(max_length=255, blank=True, null=False, default='complemento não informado')
    NumeroCasa = models.IntegerField(null=False, default='Numero da Casa não informado')


    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username

    @staticmethod
    def criar_grupos_permissoes():
        """
        Método estático para criar grupos e permissões
        automaticamente no banco de dados.
        """
        # Criar grupos
        grupo_medico, _ = Group.objects.get_or_create(name='Medico')
        grupo_paciente, _ = Group.objects.get_or_create(name='Paciente')

        # Adicionar permissões ao modelo customizado Usuario
        content_type = ContentType.objects.get_for_model(Usuario)

        # Criar permissões
        permissao_atender, _ = Permission.objects.get_or_create(
            codename='pode_atender',
            name='Pode atender consultas',
            content_type=content_type,
        )
        permissao_visualizar, _ = Permission.objects.get_or_create(
            codename='pode_visualizar_pacientes',
            name='Pode visualizar pacientes',
            content_type=content_type,
        )

        # Atribuir permissões aos grupos
        grupo_medico.permissions.add(permissao_atender, permissao_visualizar)
        grupo_paciente.permissions.add(permissao_visualizar)

        print("Grupos e permissões criados com sucesso!")


# Sinal para criar grupos e permissões ao iniciar o app
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def criar_grupos_permissoes_automaticamente(sender, **kwargs):
    """
    Executa o método criar_grupos_permissoes após a migração do banco.
    """
    if sender.name == 'usuarios':  # Nome do app
        Usuario.criar_grupos_permissoes()
