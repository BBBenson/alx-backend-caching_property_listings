from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties

@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties()
    data = [{'title': p.title, 'price': str(p.price)} for p in properties]
    return JsonResponse(data, safe=False)