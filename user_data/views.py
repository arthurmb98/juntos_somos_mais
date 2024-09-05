from rest_framework.response import Response
from user_data.load_data import populate_json, populate_csv
from user_data.services import UserService
from rest_framework.decorators import api_view
import json

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'}, status=200)

@api_view(['GET'])
def get_users(request):
    user_service = UserService()
    users = user_service.get_all_users()
    return Response(users)

@api_view(['POST'])
def create_user(request):
    try:
        user_data = request.data
        user_service = UserService()
        user = user_service.create_user(user_data)
        return Response(user, status=201)
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=400)

@api_view(['POST'])
def populate_database_view(request):
    if request.method == 'POST':
        try:
            populate_json()
            populate_csv()
            return Response({'status': 'success', 'message': 'Database populated successfully'}, status=200)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
    return Response({'status': 'error', 'message': 'POST request required'}, status=400)

@api_view(['POST'])
def populate_csv_view(request):
    if request.method == 'POST':
        try:
            populate_csv()
            return Response({'status': 'success', 'message': 'Database populated successfully'}, status=200)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
    return Response({'status': 'error', 'message': 'POST request required'}, status=400)

@api_view(['POST'])
def populate_json_view(request):
    if request.method == 'POST':
        try:
            populate_json()
            return Response({'status': 'success', 'message': 'Database populated successfully'}, status=200)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
    return Response({'status': 'error', 'message': 'POST request required'}, status=400)

@api_view(['GET'])
def purge_users_view(request):
    try:
        # Expurga todos os dados (ou utilize outra lógica para definir quais dados expurgar)
        user_service = UserService()
        response = user_service.purge_users()  # Ou user_service.purge_old_users(date_threshold)
        return Response(response, status=200)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)