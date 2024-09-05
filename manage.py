#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django



def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juntos_somos_mais.settings')  # Substitua 'your_project' pelo nome do seu projeto
    django.setup()

    from user_data.models import User
    from user_data.load_data import populate_json, populate_csv
    # Limpar o banco de dados
    User.objects.all().delete()
    # Popula o banco de dados
    populate_json()
    populate_csv()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()


