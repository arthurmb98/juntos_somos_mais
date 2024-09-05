
from user_data.models import User
from user_data.utils import *

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
            phone=format_phone_number(user['telephoneNumbers'][0]),
            cell=format_phone_number(user['mobileNumbers'][0]),
            picture_large=user['picture']['large'],
            picture_medium=user['picture']['medium'],
            picture_thumbnail=user['picture']['thumbnail']
        )
        db_user.save()  # Salvar o usuário no banco de dados

        
def populate_csv():
    csv_url = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv'
   
    try:
        csv_content = download_file(csv_url)
        
        csv_data = read_csv(csv_content)
        
        transformed_csv_data = transform_csv_data(csv_data)
        
        insert_users(transformed_csv_data)
    
    except Exception as e:
        print(f"An error occurred inserting CSV: {e}")
                
def populate_json():
    json_url = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json'
    
    try:
        json_content = download_file(json_url)
        json_data = read_json(json_content)
        transformed_json_data = transform_json_data(json_data)
        insert_users(transformed_json_data)
    
    except Exception as e:
        print(f"An error occurred inserting JSON: {e}")