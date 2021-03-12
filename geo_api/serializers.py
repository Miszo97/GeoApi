from rest_framework import serializers

from geo_api.models import IPGeoData


class IPGeoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPGeoData
        fields = '__all__'
