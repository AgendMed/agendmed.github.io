from datetime import date
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render



class Usuario(AbstractUser):
    nome_completo = models.CharField(max_length=150, null=False, default='Nome não informado')
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=30, blank=True, null=False, default='Telefone não informado')
    data_nascimento = models.DateField(verbose_name="Data de nascimento", default=date(2000, 1, 1), null=False)
    bairro = models.TextField(max_length=255, blank=True, null=False, default='Bairro não informado')
    rua = models.TextField(max_length=255, blank=True, null=False, default='Rua não informada')
    complemento = models.TextField(max_length=255, blank=True, null=False, default='complemento não informado')
    numerocasa = models.CharField(max_length=20, null=False, default='Numero da Casa não informado')


    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username

    @staticmethod
    def criar_grupos_permissoes():
        """
        Método estático para criar grupos e permissões automaticamente no banco de dados.
        """
        # Criar grupos
        grupo_medico, _ = Group.objects.get_or_create(name='Medico')
        grupo_paciente, _ = Group.objects.get_or_create(name='Paciente')
        grupo_unidade_saude, _ = Group.objects.get_or_create(name='Unidade_Saude')
        grupo_admin, _ = Group.objects.get_or_create(name='Admin')

        # Adicionar permissões ao modelo customizado Usuario
        content_type = ContentType.objects.get_for_model(Usuario)

        # Criar permissões para médicos e pacientes
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

        # Criar permissões para a Unidade de Saúde
        permissao_gerenciar_pacientes, _ = Permission.objects.get_or_create(
            codename='pode_gerenciar_pacientes',
            name='Pode gerenciar pacientes',
            content_type=content_type,
        )
        permissao_gerenciar_consultas, _ = Permission.objects.get_or_create(
            codename='pode_gerenciar_consultas',
            name='Pode gerenciar consultas',
            content_type=content_type,
        )

        # Criar permissões para administradores
        permissao_gerenciar_usuarios, _ = Permission.objects.get_or_create(
            codename='pode_gerenciar_usuarios',
            name='Pode gerenciar usuários',
            content_type=content_type,
        )
        permissao_gerenciar_unidades, _ = Permission.objects.get_or_create(
            codename='pode_gerenciar_unidades',
            name='Pode gerenciar unidades de saúde',
            content_type=content_type,
        )

        # Atribuir permissões aos grupos
        grupo_medico.permissions.add(permissao_atender, permissao_visualizar)
        grupo_paciente.permissions.add(permissao_visualizar)
        grupo_unidade_saude.permissions.add(permissao_gerenciar_pacientes, permissao_gerenciar_consultas)
        grupo_admin.permissions.add(permissao_gerenciar_usuarios, permissao_gerenciar_unidades)

        print("Grupos e permissões criados com sucesso!")


@receiver(post_migrate)
def criar_grupos_permissoes_automaticamente(sender, **kwargs):
    """
    Executa o método criar_grupos_permissoes após a migração do banco.
    """
    if sender.name == 'users':
        Usuario.criar_grupos_permissoes()


# Para garantir que o usuário tem a permissão 'pode_gerenciar_usuarios'
@permission_required('users.pode_gerenciar_usuarios', raise_exception=True)
def gerenciar_usuarios(request):
    # Lógica para gerenciar usuários
    return render(request, 'gerenciar_usuarios.html')

