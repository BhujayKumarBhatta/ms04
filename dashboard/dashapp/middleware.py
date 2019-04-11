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

from .utils import get_last_activity, set_last_activity

class DashboradMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print(exception.__class__.__name__)
        #print(exception.message)
        print('Testin Kiran  .......')
        now = datetime.now()
        if '_session_security' not in request.session:
            set_last_activity(request.session, now)
            return
        delta = now - get_last_activity(request.session)
        expire_seconds = self.get_expire_seconds(request)
        if delta >= timedelta(seconds=expire_seconds):
            logout(request)
        elif (request.path == reverse('session_security_ping') and
                'idleFor' in request.GET):
            self.update_last_activity(request, now)
        elif not self.is_passive_request(request):
            set_last_activity(request.session, now)
    
        return None


    def get_expire_seconds(self, request):
        """Return time (in seconds) before the user should be logged out."""
        return EXPIRE_AFTER


    def update_last_activity(self, request, now):
        """
        If ``request.GET['idleFor']`` is set, check if it refers to a more
        recent activity than ``request.session['_session_security']`` and
        update it in this case.
        """
        last_activity = get_last_activity(request.session)
        server_idle_for = (now - last_activity).seconds

        # Gracefully ignore non-integer values
        try:
            client_idle_for = int(request.GET['idleFor'])
        except ValueError:
            return

        # Disallow negative values, causes problems with delta calculation
        if client_idle_for < 0:
            client_idle_for = 0

        if client_idle_for < server_idle_for:
            # Client has more recent activity than we have in the session
            last_activity = now - timedelta(seconds=client_idle_for)

        # Update the session
        set_last_activity(request.session, last_activity)