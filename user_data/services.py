import csv
import json
import requests
from io import StringIO
from django.core.files.base import ContentFile
from .models import User

def process_csv(file_content):
    data = csv.DictReader(StringIO(file_content))
    for row in data:
        process_row(row)

def process_json(file_url):
    response = requests.get(file_url)
    data = response.json()
    for item in data:
        process_row(item)

def process_row(row):
    # Exemplo de transformação
    user = User(
        gender='M' if row['gender'] == 'male' else 'F',
        name_title=row['name.title'],
        name_first=row['name.first'],
        name_last=row['name.last'],
        location_street=row['location.street'],
        location_city=row['location.city'],
        location_state=row['location.state'],
        location_postcode=row['location.postcode'],
        location_coordinates_latitude=float(row['location.coordinates.latitude']),
        location_coordinates_longitude=float(row['location.coordinates.longitude']),
        location_timezone_offset=row['location.timezone.offset'],
        location_timezone_description=row['location.timezone.description'],
        email=row['email'],
        birthday=row['dob.date'],
        registered=row['registered.date'],
        telephone_numbers=[convert_phone_number(row['phone'])],
        mobile_numbers=[convert_phone_number(row['cell'])],
        picture_large=row['picture.large'],
        picture_medium=row['picture.medium'],
        picture_thumbnail=row['picture.thumbnail'],
    )
    user.save()

def convert_phone_number(phone_number):
    # Lógica para converter números de telefone
    return phone_number  # Modifique conforme necessário
