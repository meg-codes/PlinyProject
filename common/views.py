from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.utils.http import urlencode
import requests


def get_country(request):

    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if not ip:
        ip = request.META.get('REMOTE_ADDR', None)

    if ip:

        try:
            validate_ipv46_address(ip)
        except ValidationError:
            return HttpResponse('')

        query_string = {
            'access_key': settings.IPSTACK_KEY,
            'fields': "country_code"
        }
        res = requests.get('http://api.ipstack.com/%s?%s' %
                          (ip, urlencode(query_string)))
        if res.status_code == 200 and res.json()['country_code']:
            return HttpResponse('%s' % res.json()['country_code'])

    return HttpResponse('')
