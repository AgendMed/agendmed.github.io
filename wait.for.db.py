import os
import sys
import time
import psycopg2
from urllib.parse import urlparse
from django.core.management import call_command

def apply_migrations():
    print("🚀 Aplicando migrações FORÇADAMENTE")
    try:
        call_command('makemigrations', interactive=False)
        call_command('migrate', interactive=False, fake=False)
        call_command('showmigrations')
        return True
    except Exception as e:
        print(f"💥 ERRO NAS MIGRAÇÕES: {str(e)}")
        return False

def wait_for_db():
    max_retries = 15  # Aumentei o número de tentativas
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL não encontrada!")
        return False

    print("🔄 Conectando ao banco de dados...")
    
    for i in range(max_retries):
        try:
            url = urlparse(DATABASE_URL)
            conn = psycopg2.connect(
                dbname=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port,
                connect_timeout=5
            )
            conn.close()
            print("✅ Conexão bem-sucedida!")
            
            # Forçar migrações após conexão
            if apply_migrations():
                return True
            else:
                return False
                
        except Exception as e:
            print(f"⚠️ Tentativa {i+1}/{max_retries}: {str(e)}")
            time.sleep(5)
    
    print("❌ Falha crítica: não foi possível conectar ao banco")
    return False

if __name__ == "__main__":
    if not wait_for_db():
        sys.exit(1)  # Falha crítica - aborta o deploy