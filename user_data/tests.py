from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class UserDataTests(APITestCase):

    def test_health_check(self):
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_load_data(self):
        response = self.client.get(reverse('load_data'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users(self):
        self.client.get(reverse('load_data'))  # Carregar dados antes de listar
