import pandas as pd
import json
from .models import User

def process_csv(file):
    df = pd.read_csv(file)
    for _, row in df.iterrows():
        User.objects.create(
            type=determine_type(row['longitude'], row['latitude']),
            gender='M' if row['gender'] == 'male' else 'F',
            name_title=row['name.title'],
            name_first=row['name.first'],
            name_last=row['name.last'],
            street=row['location.street'],
            city=row['location.city'],
            state=row['location.state'],
            postcode=row['location.postcode'],
            latitude=row['location.coordinates.latitude'],
            longitude=row['location.coordinates.longitude'],
            timezone_offset=row['location.timezone.offset'],
            timezone_description=row['location.timezone.description'],
            email=row['email'],
            birthday=row['dob.date'],
            registered=row['registered.date'],
            telephone_numbers=[convert_to_e164(row['phone'])],
            mobile_numbers=[convert_to_e164(row['cell'])],
            picture_large=row['picture.large'],
            picture_medium=row['picture.medium'],
            picture_thumbnail=row['picture.thumbnail'],
        )

def process_json(file):
    data = json.load(file)
    for entry in data:
        User.objects.create(
            type=determine_type(entry['location']['coordinates']['longitude'], entry['location']['coordinates']['latitude']),
            gender='M' if entry['gender'] == 'male' else 'F',
            name_title=entry['name']['title'],
            name_first=entry['name']['first'],
            name_last=entry['name']['last'],
            street=entry['location']['street'],
            city=entry['location']['city'],
            state=entry['location']['state'],
            postcode=entry['location']['postcode'],
            latitude=entry['location']['coordinates']['latitude'],
            longitude=entry['location']['coordinates']['longitude'],
            timezone_offset=entry['location']['timezone']['offset'],
            timezone_description=entry['location']['timezone']['description'],
            email=entry['email'],
            birthday=entry['dob']['date'],
            registered=entry['registered']['date'],
            telephone_numbers=[convert_to_e164(entry['phone'])],
            mobile_numbers=[convert_to_e164(entry['cell'])],
            picture_large=entry['picture']['large'],
            picture_medium=entry['picture']['medium'],
            picture_thumbnail=entry['picture']['thumbnail'],
        )

def convert_to_e164(phone_number):
    # Implement conversion logic
    return phone_number

def determine_type(longitude, latitude):
    # Implement classification logic
    return 'traballhoso'
