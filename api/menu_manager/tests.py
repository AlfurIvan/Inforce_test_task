"""Menu Manager Tests"""
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class TestMenuFetchOrderApi(APITestCase):
    def test_unauthorized_user_tries_create_order(self):
        """Forbidding unauthorised requests"""
        sample_input = {'id': 3}
        response = self.client.post(reverse('order'), sample_input)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_menus(self):
        """Testing correctness of permissions.IsAuthenticatedOrReadOnly"""
        response = self.client.get('/lunch/menus/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestMenuUploadApi(APITestCase):
    def test_unauthorized_user_tries_create_menu(self):
        """Forbidding unauthorised requests"""
        sample_input = {'id': 3}
        response = self.client.post(reverse('order'), sample_input)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class OrdersAmountApi(APITestCase):
    def test_unauthorized_user_tries_fetch_total_orders(self):
        """Forbidding unauthorised requests"""
        response = self.client.get(reverse('total'))
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
