import csv
import json
import requests
from io import StringIO
import pytz
import re
from datetime import datetime

def parse_datetime(date_str: str) -> datetime:
    if date_str:
        try:
            naive_datetime = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')  # Ajuste o formato conforme o seu JSON
            return pytz.utc.localize(naive_datetime)  # Adiciona fuso horário UTC
        except (ValueError, TypeError):
            print(f"Date parsing error for value: {date_str}")  # Linha de depuração
            return None
    return None

def format_phone_number(phone_number: str) -> str:
    # Remove todos os caracteres não numéricos
    digits = re.sub(r'\D', '', phone_number)
    
    return f'+55{digits}'

def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error downloading file from {url}: {e}")
        raise

def read_csv(content):
    print("Tipo de conteúdo:", type(content))
    print("Conteúdo:", content)
    
    if isinstance(content, bytes):
        # Decodifica o conteúdo binário para uma string, removendo o BOM se presente
        content_str = content.decode('utf-8-sig')
        
        # Usa StringIO para tratar a string como um arquivo
        csv_file = StringIO(content_str)
        
        # Cria um leitor de CSV
        csv_reader = csv.DictReader(csv_file)
        
        # Converte o leitor em uma lista de dicionários
        data = list(csv_reader)
        
        return data
    else:
        raise ValueError("Expected content to be bytes, got {0}".format(type(content)))


def read_json(content):
    content_str = content.decode('utf-8')  # Decodificar bytes para string
    return json.loads(content_str)         # Carregar JSON da string

def transform_json_data(json_content):
    # Acesse a lista de resultados dentro do JSON
    json_content = json_content.get("results", [])
    
    if not isinstance(json_content, list):
        raise ValueError("O conteúdo JSON deve ser uma lista de objetos (dicionários).")
    
    transformed_data = []

    for item in json_content:
        if not isinstance(item, dict):
            raise ValueError(f"Esperado um dicionário, mas recebeu {type(item)}: {item}")

        transformed_item = {
            "gender": item.get('gender', '').strip().lower(),
            "name": {
                "title": item.get('name', {}).get('title', '').strip(),
                "first": item.get('name', {}).get('first', '').strip(),
                "last": item.get('name', {}).get('last', '').strip()
            },
            "location": {
                "street": item.get('location', {}).get('street', '').strip(),
                "city": item.get('location', {}).get('city', '').strip(),
                "state": item.get('location', {}).get('state', '').strip(),
                "postcode": item.get('location', {}).get('postcode', 0),  # Convert to integer
                "coordinates": {
                    "latitude": item.get('location', {}).get('coordinates', {}).get('latitude', '').strip(),
                    "longitude": item.get('location', {}).get('coordinates', {}).get('longitude', '').strip()
                },
                "timezone": {
                    "offset": item.get('location', {}).get('timezone', {}).get('offset', '').strip(),
                    "description": item.get('location', {}).get('timezone', {}).get('description', '').strip()
                }
            },
            "email": item.get('email', '').strip(),
            "birthday": item.get('dob', {}).get('date', '').strip(),
            "registered": item.get('registered', {}).get('date', '').strip(),
            "telephoneNumbers": [item.get('phone', '').strip()],
            "mobileNumbers": [item.get('cell', '').strip()],
            "picture": {
                "large": item.get('picture', {}).get('large', '').strip(),
                "medium": item.get('picture', {}).get('medium', '').strip(),
                "thumbnail": item.get('picture', {}).get('thumbnail', '').strip()
            },
            "nationality": "BR"
        }
        transformed_data.append(transformed_item)
    
    return transformed_data

def transform_csv_data(csv_data):
    transformed_data = []

    for row in csv_data:
        transformed_item = {
            "gender": row.get('gender', '').strip().lower(),
            "name": {
                "title": row.get('name__title', '').strip(),
                "first": row.get('name__first', '').strip(),
                "last": row.get('name__last', '').strip()
            },
            "location": {
                "street": row.get('location__street', '').strip(),
                "city": row.get('location__city', '').strip(),
                "state": row.get('location__state', '').strip(),
                "postcode": row.get('location__postcode', ''),
                "coordinates": {
                    "latitude": str(row.get('location__coordinates__latitude', '')).strip(),
                    "longitude": str(row.get('location__coordinates__longitude', '')).strip()
                },
                "timezone": {
                    "offset": row.get('location__timezone__offset', '').strip(),
                    "description": row.get('location__timezone__description', '').strip()
                }
            },
            "email": row.get('email', '').strip(),
            "birthday": row.get('dob__date', '').strip(),
            "registered": row.get('registered__date', '').strip(),
            "telephoneNumbers": [row.get('phone', '').strip()],
            "mobileNumbers": [row.get('cell', '').strip()],
            "picture": {
                "large": row.get('picture__large', '').strip(),
                "medium": row.get('picture__medium', '').strip(),
                "thumbnail": row.get('picture__thumbnail', '').strip()
            },
            "nationality": "BR"
        }
        transformed_data.append(transformed_item)
    
    return transformed_data



