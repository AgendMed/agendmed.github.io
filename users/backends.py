from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

<<<<<<< HEAD
User  = get_user_model()
=======
User = get_user_model()
>>>>>>> ed0684d553c3c83e57c0610639323e0c1eedf970

class CPFBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Tente encontrar o usuário pelo CPF
            user = User.objects.get(cpf=username)
        except User.DoesNotExist:
            return None

        # Verifique a senha
        if user.check_password(password):
<<<<<<< HEAD
            return user
        return None
=======
            # Verifique se o usuário pertence a um dos grupos
            if user.groups.filter(name='Medico').exists():
                user.group = 'Medico'
            elif user.groups.filter(name='Paciente').exists():
                user.group = 'Paciente'
            elif user.groups.filter(name='Unidade_Saude').exists():
                user.group = 'Unidade_Saude'
            elif user.groups.filter(name='Admin').exists():
                user.group = 'Admin'
            else:
                # Se o usuário não pertence a nenhum grupo válido
                return None

            return user
        
        return None
>>>>>>> ed0684d553c3c83e57c0610639323e0c1eedf970
