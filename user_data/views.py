import requests
import csv
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

# Variáveis globais para armazenar dados em memória
USERS = []

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def load_data(request):
    global USERS
    # Carregar CSV
    csv_url = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv'
    response = requests.get(csv_url)
    csv_data = response.text.splitlines()
    csv_reader = csv.DictReader(csv_data)

    # Processar CSV
    for row in csv_reader:
        user = {
            'gender': 'm' if row['gender'] == 'male' else 'f',
            'name': {
                'title': row['name.title'],
                'first': row['name.first'],
                'last': row['name.last'],
            },
            'location': {
                'street': row['location.street'],
                'city': row['location.city'],
                'state': row['location.state'],
                'postcode': int(row['location.postcode']),
                'coordinates': {
                    'latitude': row['location.coordinates.latitude'],
                    'longitude': row['location.coordinates.longitude'],
                },
                'timezone': {
                    'offset': row['location.timezone.offset'],
                    'description': row['location.timezone.description'],
                },
            },
            'email': row['email'],
            'birthday': row['dob.date'],
            'registered': row['registered.date'],
            'telephoneNumbers': [row['phone'].replace('(', '+55').replace(')', '').replace('-', '')],
            'mobileNumbers': [row['cell'].replace('(', '+55').replace(')', '').replace('-', '')],
            'picture': {
                'large': row['picture.large'],
                'medium': row['picture.medium'],
                'thumbnail': row['picture.thumbnail'],
            },
            'nationality': 'BR'
        }
        USERS.append(user)

    # Carregar JSON
    json_url = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json'
    response = requests.get(json_url)
    json_data = response.json()

    # Processar JSON
    user = {
        'gender': 'm' if json_data['gender'] == 'male' else 'f',
        'name': json_data['name'],
        'location': json_data['location'],
        'email': json_data['email'],
        'birthday': json_data['dob']['date'],
        'registered': json_data['registered']['date'],
        'telephoneNumbers': [json_data['phone'].replace('(', '+55').replace(')', '').replace('-', '')],
        'mobileNumbers': [json_data['cell'].replace('(', '+55').replace(')', '').replace('-', '')],
        'picture': json_data['picture'],
        'nationality': 'BR'
    }
    USERS.append(user)

    return Response({'status': 'data loaded'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_users(request):
    # Paginação
    page_size = int(request.query_params.get('pageSize', 10))
    page_number = int(request.query_params.get('pageNumber', 1))
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    paginated_users = USERS[start_index:end_index]

    # Serialização
    serializer = UserSerializer(paginated_users, many=True)

    response_data = {
        'pageNumber': page_number,
        'pageSize': page_size,
        'totalCount': len(USERS),
        'users': serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)
