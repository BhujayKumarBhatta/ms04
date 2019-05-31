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
#### For File Upload
from django.conf import settings
from django.conf.urls.static import static
## End
from django.urls import path
from . import views
#from rest_framework_swagger.views import get_swagger_view
#from rest_framework.documentation import include_docs_urls

#schema_view = get_swagger_view(title='TSP Billing')
app_name = 'dashapp'
urlpatterns = [path('', views.login, name='login'),
               path('', views.logout, name='logout'),
    #Infops DB
    path('home2', views.home2, name='home2'),

    path('list_links', views.list_links, name='list_links'),
    path('managelocalnet', views.managelocalnet, name='managelocalnet'),
    path('manageaddress', views.manageaddress, name='manageaddress'),
    path('managerate', views.managerate, name='managerate'),
    path('managepayment', views.managepayment, name='managepayment'),
    path('listobjects', views.listobjects, name='listobjects'),
    
    path('list_test', views.list_links, name='list_test'),      
    #Token Leader
    path('list_users', views.list_users, name='list_users'),
    path('adduser', views.adduser, name='adduser'),
    path('list_org', views.list_org, name='list_org'),
    path('list_dept', views.list_dept, name='list_dept'), 
    path('list_role', views.list_role, name='list_role'),
    path('list_ou', views.list_ou, name='list_ou'),
    #Div Invoice
    path('list_divinvoices', views.list_divinvoices, name='list_divinvoices'),
    path('invoicediv_delete', views.invoicediv_delete, name='invoicediv_delete'),
    #Invoice
    path('sampleinvoice', views.sampleinvoice, name='sampleinvoice'),
    path('list_invoices', views.list_invoices, name='list_invoices'),
    path('list_invoices_rcom', views.list_invoices_rcom, name='list_invoices_rcom'),    
    path('invoice_upload', views.invoice_upload, name='invoice_upload'),
    path('view_upload', views.view_upload, name='view_upload'),
    path('invoice_dwndformat', views.invoice_dwndformat, name='invoice_dwndformat'),   

    path('invoice_update_upload', views.invoice_update_upload, name='invoice_update_upload')
    ,path('invoice_rcom_upload', views.invoice_rcom_upload, name='invoice_rcom_upload')
    ,path('add_model', views.add_model, name='add_model')    
    ,path('invoice_delete', views.invoice_delete, name='invoice_delete')
    ,path('invoice_create', views.invoice_create, name='invoice_create')
    ,path('invoice_approvals', views.invoice_approvals, name='invoice_approvals')
    ,path('invoice_approve', views.invoice_approve, name='invoice_approve')
    ,path('invoice_reject', views.invoice_reject, name='invoice_reject')
    #,path('swagger-docs/', schema_view)
    #,path('docs/', include_docs_urls(title='TSP Billing'))
    ]



#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
