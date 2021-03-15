from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from geo_api.models import IPGeoData

# Create your tests here.


class RegisterViewTest(TestCase):
    def test_correct_payload(self):
        res = self.client.post(
            '/register', {'username': 'jack', 'password': 'orange'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_incorrect_payload(self):
        res = self.client.post(
            '/register', {'usernxxame': 'jack', 'password': 'orange'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class GeoDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user('jack', 'sparrow')
        self.client.force_authenticate(user=user)

    def test_add_adderess_not_present_in_database(self):
        res = self.client.post(
            '/addresses/', {'address': '172.217.3.197'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_add_address_present_in_database(self):
        IPGeoData.objects.create(ip='172.217.3.197', latitude=12, longitude=15)

        res = self.client.post(
            '/addresses/', {'address': '172.217.3.197'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_addresses_present_in_database(self):
        res = self.client.get("/addresses/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_incorrect_addresss(self):
        res = self.client.post(
            '/addresses/', {'address': '172217.3.197'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_payload(self):
        res = self.client.post(
            '/addresses/', {'adres': '172.217.3.197'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class GeoDataDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user('jack', 'sparrow')
        self.client.force_authenticate(user=user)

    def test_get_address_present_in_database(self):
        '''
        Requester asks for geo data of an address which is the database
        '''
        IPGeoData.objects.create(ip='172.217.3.197', latitude=12, longitude=15)

        res = self.client.get("/addresses/172.217.3.197")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_address_not_present_in_database(self):
        '''
        Requester asks for geo data of an address which is not in the database
        '''

        res = self.client.get("/addresses/www.google.com")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
