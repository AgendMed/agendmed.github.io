import os
import django
from django.db import connection
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgendMed.settings')
django.setup()

def apply_migrations():
    print("🔍 Verificando migrações pendentes...")
    try:
        call_command('makemigrations', interactive=False, verbosity=0)
        call_command('migrate', interactive=False, verbosity=0)
        
        # Verifica se a tabela existe
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'Unidade_Saude_unidadesaude'
                )
            """)
            if not cursor.fetchone()[0]:
                print("⚠️ Tabela ainda não existe - aplicando migrações novamente")
                call_command('migrate', interactive=False, verbosity=2)
        
        return True
    except Exception as e:
        print(f"❌ Erro nas migrações: {str(e)}")
        return False

if __name__ == '__main__':
    apply_migrations()