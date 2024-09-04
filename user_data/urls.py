from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check),
    path('load_data/', views.load_data),
    path('users/', views.list_users),
]
