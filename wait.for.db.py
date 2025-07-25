import os
import time
import psycopg2
from urllib.parse import urlparse
from django.core.management import call_command

def wait_for_db():
    max_retries = 10
    retry_count = 0
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    print("🔄 Aguardando banco de dados...")
    
    while retry_count < max_retries:
        try:
            url = urlparse(DATABASE_URL)
            conn = psycopg2.connect(
                dbname=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port,
                connect_timeout=3
            )
            conn.close()
            print("✅ Banco conectado!")
            
            # FORÇAR MIGRAÇÕES AQUI MESMO
            print("🔄 Aplicando migrações...")
            call_command('makemigrations', interactive=False)
            call_command('migrate', interactive=False)
            call_command('showmigrations')
            
            return True
            
        except Exception as e:
            retry_count += 1
            print(f"⚠️ Tentativa {retry_count}/{max_retries}: {str(e)}")
            time.sleep(5)
    
    print("❌ Falha ao conectar ao banco")
    return False

if __name__ == "__main__":
    wait_for_db()