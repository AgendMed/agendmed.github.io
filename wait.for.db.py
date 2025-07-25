import os
import time
import psycopg2
from urllib.parse import urlparse
from django.core.management import call_command
from django.core.management.base import CommandError

def wait_for_db():
    max_retries = 10
    retry_count = 0
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL não está definida")
        return False
    
    print("🔄 Aguardando banco de dados ficar disponível...")
    
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
            print("✅ Banco conectado com sucesso!")
            return True
            
        except Exception as e:
            retry_count += 1
            print(f"⚠️ Tentativa {retry_count}/{max_retries}: {str(e)}")
            time.sleep(5)
    
    print("❌ Falha ao conectar ao banco de dados")
    return False

if __name__ == "__main__":
    if wait_for_db():
        try:
            print("🔄 Criando migrações...")
            call_command('makemigrations', interactive=False)
            print("🔄 Aplicando migrações...")
            call_command('migrate', interactive=False)
            print("✅ Migrações aplicadas com sucesso!")
        except CommandError as e:
            print(f"❌ Erro ao aplicar migrações: {str(e)}")
            exit(1)
    else:
        exit(1)