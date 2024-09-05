import pytz
from datetime import datetime
from user_data.models import User
from user_data.utils import download_file, transform_json_data, read_csv, read_json

def parse_datetime(date_str: str) -> datetime:
    if date_str:
        try:
            naive_datetime = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')  # Ajuste o formato conforme o seu JSON
            return pytz.utc.localize(naive_datetime)  # Adiciona fuso horário UTC
        except (ValueError, TypeError):
            print(f"Date parsing error for value: {date_str}")  # Linha de depuração
            return None
    return None

def insert_users(data):
    for user in data:
        db_user = User(
            gender=user['gender'],
            title=user['name']['title'],
            first_name=user['name']['first'],
            last_name=user['name']['last'],
            street=user['location']['street'],
            city=user['location']['city'],
            state=user['location']['state'],
            postcode=user['location']['postcode'],
            latitude=user['location']['coordinates']['latitude'],
            longitude=user['location']['coordinates']['longitude'],
            timezone_offset=user['location']['timezone']['offset'],
            timezone_description=user['location']['timezone']['description'],
            email=user['email'],
            birthday=parse_datetime(user['birthday']),
            registered=parse_datetime(user['registered']),
            phone=user['telephoneNumbers'][0],
            cell=user['mobileNumbers'][0],
            picture_large=user['picture']['large'],
            picture_medium=user['picture']['medium'],
            picture_thumbnail=user['picture']['thumbnail']
        )
        db_user.save()  # Salvar o usuário no banco de dados


def populate_database():
    # URLs dos arquivos CSV e JSON
    csv_url = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv'
    json_url = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json'
    
    # Baixar e ler os dados
    #csv_data = read_csv(download_file(csv_url))
    json_data = read_json(download_file(json_url))
    
    # Transformar os dados
    #transformed_csv_data = transform_csv_data(csv_data)
    transformed_json_data = transform_json_data(json_data)
    
    # Inserir os dados no banco de dados
    insert_users(transformed_json_data)
