import csv
from datetime import datetime
from io import StringIO
import json
from typing import List, Dict, Any
from django.core.files.base import ContentFile
from .models import User

class UserService:
    def __init__(self):
        pass  # No need for a database session in Django, it uses Django ORM directly

    def get_all_users(self) -> List[Dict[str, Any]]:
        users = User.objects.all()
        return [self._convert_user_to_dict(user) for user in users]

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        def parse_date(date_str: str) -> datetime:
            if date_str:
                try:
                    return datetime.strptime(date_str, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    print(f"Date parsing error for value: {date_str}")  # Debugging line
                    return None
            return None

        db_user = User(
            gender=user_data.get('gender', ''),
            title=user_data.get('name', {}).get('title', ''),
            first_name=user_data.get('name', {}).get('first', ''),
            last_name=user_data.get('name', {}).get('last', ''),
            street=user_data.get('location', {}).get('street', ''),
            city=user_data.get('location', {}).get('city', ''),
            state=user_data.get('location', {}).get('state', ''),
            postcode=user_data.get('location', {}).get('postcode', 0),
            latitude=user_data.get('location', {}).get('coordinates', {}).get('latitude', ''),
            longitude=user_data.get('location', {}).get('coordinates', {}).get('longitude', ''),
            timezone_offset=user_data.get('location', {}).get('timezone', {}).get('offset', ''),
            timezone_description=user_data.get('location', {}).get('timezone', {}).get('description', ''),
            email=user_data.get('email', ''),
            registered=parse_date(user_data.get('registered', {}).get('date', '')),
            phone=user_data.get('telephoneNumbers', [])[0] if user_data.get('telephoneNumbers') else '',
            cell=user_data.get('mobileNumbers', [])[0] if user_data.get('mobileNumbers') else '',
            picture_large=user_data.get('picture', {}).get('large', ''),
            picture_medium=user_data.get('picture', {}).get('medium', ''),
            picture_thumbnail=user_data.get('picture', {}).get('thumbnail', '')
        )
        db_user.save()
        return self._convert_user_to_dict(db_user)

    def _convert_user_to_dict(self, user: User) -> Dict[str, Any]:
        return {
            "type": "laborious",
            "gender": user.gender,
            "name": {
                "title": user.title,
                "first": user.first_name,
                "last": user.last_name
            },
            "location": {
                "region": "sul",  # Atualize se necessário
                "street": user.street,
                "city": user.city,
                "state": user.state,
                "postcode": user.postcode,
                "coordinates": {
                    "latitude": user.latitude,
                    "longitude": user.longitude
                },
                "timezone": {
                    "offset": user.timezone_offset,
                    "description": user.timezone_description
                }
            },
            "email": user.email,
            "birthday": user.birthday.isoformat() if user.birthday else '',
            "registered": user.registered.isoformat() if user.registered else '',
            "telephoneNumbers": [user.phone],
            "mobileNumbers": [user.cell],
            "picture": {
                "large": user.picture_large,
                "medium": user.picture_medium,
                "thumbnail": user.picture_thumbnail
            },
            "nationality": "BR"  # Atualize se necessário
        }

    def import_csv(self, csv_file: ContentFile):
        csv_data = csv_file.read().decode('utf-8')
        reader = csv.DictReader(StringIO(csv_data))
        for row in reader:
            user_data = self._parse_csv_row(row)
            self.create_user(user_data)

    def import_json(self, json_file: ContentFile):
        json_data = json_file.read().decode('utf-8')
        data = json.loads(json_data).get('results', [])
        for user_data in data:
            self.create_user(user_data)

    def _parse_csv_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        return {
            "gender": row.get('gender', ''),
            "name": {
                "title": row.get('name.title', ''),
                "first": row.get('name.first', ''),
                "last": row.get('name.last', '')
            },
            "location": {
                "street": row.get('location.street', ''),
                "city": row.get('location.city', ''),
                "state": row.get('location.state', ''),
                "postcode": int(row.get('location.postcode', 0)),
                "coordinates": {
                    "latitude": row.get('location.coordinates.latitude', ''),
                    "longitude": row.get('location.coordinates.longitude', '')
                },
                "timezone": {
                    "offset": row.get('location.timezone.offset', ''),
                    "description": row.get('location.timezone.description', '')
                }
            },
            "email": row.get('email', ''),
            "birthday": row.get('dob.date', ''),
            "registered": row.get('registered.date', ''),
            "telephoneNumbers": [row.get('phone', '')],
            "mobileNumbers": [row.get('cell', '')],
            "picture": {
                "large": row.get('picture.large', ''),
                "medium": row.get('picture.medium', ''),
                "thumbnail": row.get('picture.thumbnail', '')
            },
            "nationality": "BR"  # Atualize se necessário
        }
