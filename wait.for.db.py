import os
import time
import psycopg2
from urllib.parse import urlparse
from django.core.management import call_command

def wait_for_db():
    max_retries = 10
    retry_count = 0
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não está definida")
    
    url = urlparse(DATABASE_URL)
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                dbname=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            conn.close()
            print("✅ Banco de dados disponível!")
            
            # Aplicar migrações
            print("🔄 Aplicando migrações...")
            call_command('makemigrations', interactive=False)
            call_command('migrate', interactive=False)
            
            return True
        except Exception as e:
            retry_count += 1
            print(f"⚠️ Tentativa {retry_count}/{max_retries}: Banco não disponível - {str(e)}")
            time.sleep(5)
    
    raise Exception("❌ Não foi possível conectar ao banco de dados após várias tentativas")

if __name__ == "__main__":
    wait_for_db()