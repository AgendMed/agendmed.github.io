import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgendMed.settings')
django.setup()

def verify_database():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Conexão com o banco OK")
            
            # Verifica se a tabela existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'unidade_saude_unidadesaude'
                )
            """)
            exists = cursor.fetchone()[0]
            print(f"📦 Tabela existe? {'SIM' if exists else 'NÃO'}")
            
            return exists
    except Exception as e:
        print(f"❌ Erro no banco: {str(e)}")
        return False

if __name__ == '__main__':
    verify_database()