import json
import os

import requests
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from geo_api.helpers import getIP
from geo_api.models import IPGeoData
from geo_api.serializers import IPGeoDataSerializer


class GeoData(APIView):
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

    def post(self, request, address):
        ip = getIP(address)

        if IPGeoData.objects.filter(ip=ip).exists():
            return Response('Already exists', status=status.HTTP_400_BAD_REQUEST)

        if ip is False:
            return Response('Bad ip', status=status.HTTP_400_BAD_REQUEST)

        api_key = os.environ["IPSTACK_API_KEY"]
        url = f'http://api.ipstack.com/{ip}?access_key={api_key}&fields=main'
        response = requests.get(url)
        response_json = json.loads(response.text)

        serializer = IPGeoDataSerializer(data=response_json)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, address):
        ip = self.get_ip_geo_data(address)
        serializer = IPGeoDataSerializer(ip)
        ip.delete()

        return Response(serializer.data, status=200)
