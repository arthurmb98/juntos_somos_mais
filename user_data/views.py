from django.http import JsonResponse
from sqlalchemy.orm import Session
from database import get_db
from user_data.models import User

def health_check(request):
    return JsonResponse({'status': 'ok'}, status=200)

def get_users():
    db: Session = next(get_db())
    users = db.query(User).all()
    return users