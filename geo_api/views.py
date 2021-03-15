import json
import os

import requests
from django.contrib.auth.models import Permission, User
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from geo_api.helpers import getIP
from geo_api.models import IPGeoData
from geo_api.serializers import IPGeoDataSerializer


class IpStackAPI():
    def __init__(self) -> None:
        self.api_key = os.environ["IPSTACK_API_KEY"]

    def get_geo_data(self, ip):
        url = f'http://api.ipstack.com/{ip}?access_key={self.api_key}&fields=main'
        response = requests.get(url)
        response_json = json.loads(response.text)

        return response_json


class Register(APIView):
    def get_all_geo_api_permissions(self):
        permissions = [Permission.objects.get(name=permission) for permission in [
            'Can add ip geo data',
            'Can change ip geo data',
            'Can delete ip geo data',
            'Can view ip geo data'
        ]]

        return permissions

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            error_message = json.dumps({'details': 'key error'})
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        user_already_exists = User.objects.filter(
            username=username, password=password).exists()

        if user_already_exists:
            error_message = json.dumps({'details': 'user already exists'})
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username,
                                        password=password)

        permissions = self.get_all_geo_api_permissions()

        user.user_permissions.set(permissions)

        return_message = json.dumps({'details': 'created'})
        return Response(return_message, status=status.HTTP_201_CREATED)


class GeoDataDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_ip_geo_data(self, address):
        try:
            return IPGeoData.objects.get(ip=getIP(address))
        except IPGeoData.DoesNotExist:
            raise Http404

    def get(self, request, address):
        ip = self.get_ip_geo_data(address)
        serializer = IPGeoDataSerializer(ip)
        return Response(serializer.data, status=200)

    def delete(self, request, address):
        ip = self.get_ip_geo_data(address)
        serializer = IPGeoDataSerializer(ip)
        ip.delete()

        return Response(serializer.data, status=200)


class GeoData(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        addresses = IPGeoData.objects.all()
        ser = IPGeoDataSerializer(addresses, many=True)

        response = ser.data
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            address = request.data['address']
        except KeyError:
            error_message = json.dumps({'details': 'key error'})
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        ip = getIP(address)

        if IPGeoData.objects.filter(ip=ip).exists():
            error_message = json.dumps({'details': 'ip already exists'})
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        if ip is False:
            error_message = json.dumps({'details': 'incorrect address'})
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        api = IpStackAPI()
        response_json = api.get_geo_data(ip)

        serializer = IPGeoDataSerializer(data=response_json)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
