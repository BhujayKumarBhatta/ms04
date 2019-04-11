import requests
from django.conf import settings

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
#from django_common.session import SessionManager

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
    # Works perfectly for everyone using MIDDLEWARE_CLASSES
    MiddlewareMixin = object

class DashboradMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print(exception.__class__.__name__)
        print(exception.message)
        print('Testin Kiran  .......')
        return None
