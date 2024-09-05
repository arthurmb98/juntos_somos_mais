from rest_framework.response import Response
from user_data.load_data import populate_json, populate_csv
from user_data.services import UserService
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
import json

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'}, status=200)

@api_view(['GET'])
def get_users(request):
    user_service = UserService()
    
    # Captura os parâmetros de página e tamanho da página da query string
    page_number = int(request.query_params.get('page', 1))  # Default é página 1
    page_size = int(request.query_params.get('page_size', 10))  # Default é 10 itens por página
    
    # Chama o serviço para obter os usuários paginados
    paginated_users = user_service.get_all_users(page_number=page_number, page_size=page_size)
    
    # Retorna a resposta JSON com os dados paginados
    return Response(paginated_users)

@api_view(['GET'])
def get_users_by_type(request):
    user_service = UserService()
    
    # Captura o parâmetro 'type' da query string
    user_type = request.query_params.get('type', None)
    if not user_type:
        return Response({'error': 'User type is required'}, status=400)

    # Captura os parâmetros de página e tamanho da página da query string
    page_number = int(request.query_params.get('page', 1))  # Default é página 1
    page_size = int(request.query_params.get('page_size', 10))  # Default é 10 itens por página
    
    # Chama o serviço para obter os usuários filtrados por tipo
    filtered_users = user_service.get_users_by_type(user_type=user_type, page_number=page_number, page_size=page_size)
    
    # Retorna a resposta JSON com os dados filtrados e paginados
    return Response(filtered_users)

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