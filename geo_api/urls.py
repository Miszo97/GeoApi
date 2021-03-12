from django.urls import path

from .views import GeoData

app_name = 'geo_api'

urlpatterns = [
    path('', GeoData.as_view(), name='geo_data')
]
