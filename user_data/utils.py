import csv
import json
import requests
from io import StringIO
import pandas as pd

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def read_csv(content):
    content_str = content.decode('utf-8')
    csv_reader = csv.DictReader(StringIO(content_str))
    return list(csv_reader)

def read_json(content):
    return json.loads(content)

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




