from datetime import datetime
from typing import Dict, Any, List

from user_data.utils import format_phone_number, parse_datetime
from .models import User
from django.core.paginator import Paginator

class UserService:
    def __init__(self):
        pass  # No need for a database session in Django, it uses Django ORM directly
    
    def purge_users(self):
        # Deleta todos os usuários do banco de dados
        User.objects.all().delete()
        return {'status': 'success', 'message': 'All users have been deleted'}

    def get_all_users(self, page_number: int = 1, page_size: int = 10) -> Dict[str, Any]:
        users = User.objects.all()
        
        # Cria um paginador com a lista de usuários e o tamanho da página
        paginator = Paginator(users, page_size)
        
        # Obtém a página solicitada
        page = paginator.get_page(page_number)
        
        # Converte os usuários da página para dicionários
        user_list = [self._convert_user_to_dict(user) for user in page.object_list]
        
        return {
            "pageNumber": page.number,
            "pageSize": page.paginator.per_page,
            "totalCount": page.paginator.count,
            "users": user_list
        }

    def get_users_by_type(self, user_type: str, page_number: int = 1, page_size: int = 10) -> Dict[str, Any]:
        users = User.objects.all()  # Obtém todos os usuários do banco de dados

        # Filtrar usuários dinamicamente com base no "type"
        filtered_users: List[User] = []
        for user in users:
            calculated_type = self._determine_user_type(float(user.latitude), float(user.longitude))
            if calculated_type == user_type:
                filtered_users.append(user)

        # Paginação dos usuários filtrados
        paginator = Paginator(filtered_users, page_size)
        page = paginator.get_page(page_number)

        # Converte os usuários da página para dicionários
        user_list = [self._convert_user_to_dict(user) for user in page.object_list]

        return {
            "pageNumber": page.number,
            "pageSize": page.paginator.per_page,
            "totalCount": page.paginator.count,
            "users": user_list
        }    

    def _convert_user_to_dict(self, user: User) -> Dict[str, Any]:
        # Obter as coordenadas do usuário
        latitude = float(user.latitude) if user.latitude else None
        longitude = float(user.longitude) if user.longitude else None
        # Definir o valor do atributo "type" com base nas coordenadas
        user_type = self._determine_user_type(latitude, longitude)
        
        # Converter gender para 'F' ou 'M'
        gender = 'F' if user.gender == 'female' else 'M' if user.gender == 'male' else user.gender
    
        return {
            "type": user_type,
            "gender": gender,
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

    def _determine_user_type(self, latitude: float, longitude: float) -> str:
        if latitude is None or longitude is None:
            return "laborious"  # Retorno padrão se não houver coordenadas

        # Definir limites para "special"
        special_regions = [
            {
            "minlon": -2.196998, "minlat": -46.361899, "maxlon": -15.411580, "maxlat": -34.276938
            },
            {
            "minlon": -19.766959, "minlat": -52.997614, "maxlon": -23.966413, "maxlat": -44.428305
            }
        ]

        # Verificar se está em uma região "special"
        for region in special_regions:
            if region["minlon"] <= longitude <= region["maxlon"] and region["minlat"] <= latitude <= region["maxlat"]:
                return "special"

        # Definir limites para "normal"
        normal_region = {
            "minlon": -34.016466, "minlat": -54.777426, "maxlon": -26.155681, "maxlat": -46.603598
        }

        # Verificar se está em uma região "normal"
        if normal_region["minlon"] <= longitude <= normal_region["maxlon"] and normal_region["minlat"] <= latitude <= normal_region["maxlat"]:
            return "normal"

        # Se não estiver em nenhuma região especial ou normal, retorna "laborious"
        return "laborious"
