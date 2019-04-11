from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
#from django_common.session import SessionManager

class DashboradMiddleware(object):
    def process_exception(self, request, exception):
        print(exception.__class__.__name__)
        print(exception.message)
        print('Testin Kiran  .......')
        return None
