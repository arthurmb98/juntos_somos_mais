#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import execute_from_command_line
from database import engine
from user_data.models import Base  # Ajuste para o caminho correto

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juntos_somos_mais.settings')
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f"Error: {e}")
        create_tables()  # Cria as tabelas quando iniciar o projeto


