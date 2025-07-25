import os
import time
import psycopg2
from django.core.management import call_command

def wait_for_db():
    max_retries = 15  # Aumente o número de tentativas
    db_config = {
        'dbname': 'agendmed_postgresql',
        'user': 'agendmed_user',
        'password': 'UAOYpOYCBi1Xz7XDkUO2exKlH9CAuwV8',
        'host': 'dpg-d20lqr7gi27c73cp1dag-a.oregon-postgres.render.com',
        'port': '5432',
        'connect_timeout': 5
    }
    
    print("🔄 Aguardando banco de dados...")
    
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(**db_config)
            conn.close()
            print("✅ Conexão bem-sucedida!")
            
            # Forçar migrações
            print("🔄 Aplicando migrações...")
            call_command('makemigrations', interactive=False)
            call_command('migrate', interactive=False, fake=False)
            
            # Verificar tabelas criadas
            with conn.cursor() as cursor:
                cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
                print(f"📦 Tabelas existentes: {[row[0] for row in cursor.fetchall()]}")
            
            return True
        except Exception as e:
            print(f"⚠️ Tentativa {i+1}/{max_retries}: {str(e)}")
            time.sleep(5)
    
    print("❌ Falha crítica ao conectar ao banco")
    return False

if __name__ == "__main__":
    if not wait_for_db():
        exit(1)  # Falha crítica - aborta o deploy