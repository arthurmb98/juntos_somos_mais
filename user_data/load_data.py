# user_data/management/commands/load_data.py

from django.core.management.base import BaseCommand
import csv
import json
from user_data.models import User

class Command(BaseCommand):
    help = 'Load user data from CSV and JSON files'

    def handle(self, *args, **kwargs):
        # Exemplo de como carregar dados
        self.load_csv()
        self.load_json()

    def load_csv(self):
        # Lógica para carregar dados CSV
        pass

    def load_json(self):
        # Lógica para carregar dados JSON
        pass
