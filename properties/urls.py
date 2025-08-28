from django.urls import path
from .views import property_list
from django.core.cache import cache
from .models import Property

urlpatterns = [
    path('properties/', property_list, name='property-list'),
]

def get_all_properties():
    queryset = cache.get('all_properties')
    if not queryset:
        queryset = list(Property.objects.all())
        cache.set('all_properties', queryset, 3600)
    return queryset