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
from dashapp.linkinv import  linkinv_views
from dashapp.views import paperhouse_delete_invoice
from dashapp.paperhouse import paperhouse
from dashapp.penman import penman
#from rest_framework_swagger.views import get_swagger_view
#from rest_framework.documentation import include_docs_urls

#schema_view = get_swagger_view(title='TSP Billing')
app_name = 'dashapp'
urlpatterns = [path('', views.login, name='login'),
               path('logout', views.log_out, name='logout'),
    #Infops DB
    path('home2', views.home2, name='home2'),
    
    path('list_links', views.list_links, name='list_links'),
    path('list_ravl_obj/<slug:objname>/<slug:rolename>', linkinv_views.list_ravl_obj, name='list_ravl_obj'),
    path('delete_ravl/<slug:objname>/<slug:objid>', linkinv_views.delete_ravl, name='delete_ravl'),
    path('managelocalnet', views.managelocalnet, name='managelocalnet'),
    path('add_address', linkinv_views.add_address, name='add_address'),
    path('add_rate', linkinv_views.add_rate,  name='add_rate'),
    path('add_payment', linkinv_views.add_payment,  name='add_payment'),
    
    
    path('list_test', views.list_links, name='list_test'),      
    #Token Leader
    path('add_org', views.add_org, name='add_org'),
    path('list_org', views.list_org, name='list_org'),
    path('delete_org', views.delete_org, name='delete_org'),
    path('add_ou', views.add_ou, name='add_ou'),
    path('list_ou', views.list_ou, name='list_ou'),
    path('delete_ou', views.delete_ou, name='delete_ou'),
    path('add_dept', views.add_dept, name='add_dept'),
    path('list_dept', views.list_dept, name='list_dept'),
    path('delete_dept', views.delete_dept, name='delete_dept'),
    path('add_wfc', views.add_wfc, name='add_wfc'),
    path('list_wfc', views.list_wfc, name='list_wfc'),
    path('delete_wfc', views.delete_wfc, name='delete_wfc'),
    path('add_role', views.add_role, name='add_role'),
    path('list_role', views.list_role, name='list_role'),
    path('delete_role', views.delete_role, name='delete_role'),
    path('adduser', views.adduser, name='adduser'),
    path('list_users', views.list_users, name='list_users'),
    path('adduser', views.adduser, name='adduser'),
    path('delete_user', views.delete_user, name='delete_user'),
    
    path('list_service', views.list_service, name='list_service'),
    path('add_service', views.add_service, name='add_service'),
    path('delete_service', views.delete_service, name='delete_service'),
    
  
    
    #XLuploader
    
    path('xluploader_invoice_upload', views.xluploader_invoice_upload, name='xluploader_invoice_upload'),
    path('download_invoicexlformat', views.download_invoicexlformat, name='download_invoicexlformat'),
        
    
    #penman
    path('penman_list_events',penman.list_events, name='penman_list_events'),
    path('penman_delete_events', views.penman_delete_events, name='penman_delete_events'),       
    #paperhouse
    path('paperhouse_list_invoice/<slug:invoicenum>/<slug:mode>/<slug:listype>', 
         views.paperhouse_list_invoice, name='paperhouse_list_invoice'),   
    path('paperhouse_delete_invoice', views.paperhouse_delete_invoice, name='paperhouse_delete_invoice'),    
    path('tsp_list_invoice', views.tsp_list_invoice, name='tsp_list_invoice'),
    path('paperhouse_savedraft_list/<slug:status>', 
         paperhouse.draft_list, name='paperhouse_savedraft_list'),   
    #striker
    path('striker_list_responces/<slug:request_id>', views.striker_list_responces, name='striker_list_responces'),
    path('striker_delete_responces', views.striker_delete_responces, name='striker_delete_responces'),
    path('striker_update_Invoice/<slug:actionrole>', views.striker_update_Invoice, name='striker_update_Invoice'),
    path('striker_update_from_draft/<slug:actionrole>', views.striker_update_from_Draft, name='striker_update_from_draft'),
    
    
    #,path('swagger-docs/', schema_view)
    #,path('docs/', include_docs_urls(title='TSP Billing'))
    
    path('manageaddress', views.manageaddress, name='manageaddress'),
    path('managerate', views.managerate, name='managerate'),
    path('managepayment', views.managepayment, name='managepayment'),
    path('listobjects', views.listobjects, name='listobjects'),
    
    path('listdocs', views.listdocs, name='listdocs'),
    
    ]



#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
