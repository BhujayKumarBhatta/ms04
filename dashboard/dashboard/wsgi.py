"""
WSGI config for dashboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
import activate_this

# otherwise wsgi will not be able to locate the application path and fail to import dashboard
sys.path.append('opt/dashboard/dashboard')
sys.path.append('opt/dashboard/dashboard/dashboard')

activate_this = '/opt/dashboard/venv/bin/activate_this.py'
with open(activate_this) as file:
    exec(file_.reada(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

application = get_wsgi_application()
