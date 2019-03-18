"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

app_name = 'dashapp'
urlpatterns = [path('', views.login, name='login'),
    path('list_users', views.list_users, name='list_users'),
    path('list_links', views.list_links, name='list_links'),
    path('list_test', views.list_test, name='list_test'),
    path('adduser', views.adduser, name='adduser'),
    path('list_invoices', views.list_invoices, name='invoice'),
    path('invoice_upload', views.invoice_upload, name='invoice_upload')]
