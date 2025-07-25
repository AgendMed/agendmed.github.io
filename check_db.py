import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgendMed.settings')
django.setup()

from django.db import connection

def check_db():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexão com o banco OK!")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

if __name__ == '__main__':
    check_db()