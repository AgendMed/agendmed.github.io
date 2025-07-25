import os
import time
import psycopg2
from urllib.parse import urlparse

DATABASE_URL = os.getenv('DATABASE_URL')

def wait_for_db():
    print("Aguardando banco de dados ficar disponível...")
    url = urlparse(DATABASE_URL)
    while True:
        try:
            conn = psycopg2.connect(
                dbname=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            conn.close()
            print("Banco disponível!")
            break
        except Exception as e:
            print("Banco ainda não disponível, tentando novamente em 5 segundos...")
            time.sleep(5)

if __name__ == "__main__":
    wait_for_db()
