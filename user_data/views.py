from rest_framework.response import Response
from user_data.load_data import insert_users, populate_json, populate_csv
from user_data.services import UserService
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
import json
from user_data.utils import download_file, read_csv, read_json, transform_csv_data, transform_json_data

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
def create_users(request):
    url = request.data.get('file_url')
    if not url:
        return Response({'error': 'file_url parameter is required'}, status=400)

    try:
        file_content = download_file(url)

        # Determine file type
        if url.lower().endswith('.csv'):
            csv_data = read_csv(file_content)
            transformed_data = transform_csv_data(csv_data)
        elif url.lower().endswith('.json'):
            json_data = read_json(file_content)
            transformed_data = transform_json_data(json_data)
        else:
            return Response({'error': 'Unsupported file type'}, status=400)

        # Inserir os usuários e armazenar os objetos criados
        created_users = insert_users(transformed_data)

        # Converter os usuários para o formato desejado
        user_service = UserService()  # Ou sua classe de serviço existente
        mapped_users = [user_service._convert_user_to_dict(user) for user in created_users]

        return Response(mapped_users, status=201)

    except ValueError as e:
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        return Response({'error': 'An error occurred: ' + str(e)}, status=500)


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