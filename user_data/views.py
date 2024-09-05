from django.http import JsonResponse
from user_data.load_data import populate_database
from user_data.services import UserService
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

populate_database()

@csrf_exempt  # Use com cuidado, apenas para desenvolvimento ou se você não tiver CSRF configurado
def health_check(request):
    return JsonResponse({'status': 'ok'}, status=200)

def get_users(request):
    user_service = UserService()
    users = user_service.get_all_users()
    return JsonResponse(users, safe=False)

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            user_data = json.loads(request.body)
            user_service = UserService()
            user = user_service.create_user(user_data)
            return JsonResponse(user, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'POST request required'}, status=400)

@csrf_exempt
def populate_database_view(request):
    if request.method == 'POST':
        try:
            populate_database()
            return JsonResponse({'status': 'success', 'message': 'Database populated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'POST request required'}, status=400)
