"""
WSGI config for dashboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
#import site

sys.path.append('/opt/dashboard/dashboard')
sys.path.append('/opt/dashboard/dashboard/dashboard')

from django.core.wsgi import get_wsgi_application


activate_this = '/opt/dashboard/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

application = get_wsgi_application()
