# user_data/models.py

from django.db import models

class User(models.Model):
    gender = models.CharField(max_length=10)
    name = models.JSONField()  # Exemplo para simplificação
    location = models.JSONField()
    email = models.EmailField()
    birthday = models.DateTimeField()
    registered = models.DateTimeField()
    telephone_numbers = models.JSONField()  # Exemplo para simplificação
    mobile_numbers = models.JSONField()
    picture = models.JSONField()
    nationality = models.CharField(max_length=2, default='BR')
