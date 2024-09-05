from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_users, name='get_users'),
    path('create-user/', views.create_user, name='create_user'),
    path('populate-database/', views.populate_database_view, name='populate_database'),
]