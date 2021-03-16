from django.urls import path

from .views import GeoData, GeoDataDetail

app_name = 'geo_api'

urlpatterns = [
    path('', GeoData.as_view(), name='geo_data'),
    path('<address>/', GeoDataDetail.as_view(), name='geo_data_detail'),
]
