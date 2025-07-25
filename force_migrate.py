import os
import sys
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgendMed.settings')

def run():
    print("🚀 FORÇANDO MIGRAÇÕES")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        execute_from_command_line(['manage.py', 'showmigrations'])
        return True
    except Exception as e:
        print(f"💥 ERRO: {str(e)}")
        return False

if __name__ == '__main__':
    if not run():
        sys.exit(1)