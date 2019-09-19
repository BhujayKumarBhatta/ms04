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
               path('logout', views.log_out, name='logout'),
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
    
    #XLuploader
    ,path('xluploader_invoice_upload', views.xluploader_invoice_upload, name='xluploader_invoice_upload')
    #INVStore
    ,path('invstore_list_invoices', views.invstore_list_invoices, name='invstore_list_invoices')
    ,path('invstore_list_invoice_bycurrent_lastorder', views.invstore_list_invoice_bycurrent_lastorder, name='invstore_list_invoice_bycurrent_lastorder')
    ,path('invstore_list_invoice_byfield', views.invstore_list_invoice_byfield, name='invstore_list_invoice_byfield')
    ,path('invstore_invoice_delete', views.invstore_invoice_delete, name='invstore_invoice_delete')
    ,path('invstore_list_divinvoices', views.invstore_list_divinvoices, name='invstore_list_divinvoices')
    ,path('invstore_list_stage1responces', views.invstore_list_stage1responces, name='invstore_list_stage1responces')
    ,path('invstore_delete_stage1responces', views.invstore_delete_stage1responces, name='invstore_delete_stage1responces')
    ,path('invstore_invoice_approve', views.invstore_invoice_approve, name='invstore_invoice_approve')
    ,path('invstore_invoice_reject', views.invstore_invoice_reject, name='invstore_invoice_reject')
    ,path('invstore_invoice_rcommendations', views.invstore_invoice_rcommendations, name='invstore_invoice_rcommendations')
    ,path('list_invoice_divisional_invoices', views.list_invoice_divisional_invoices, name='list_invoice_divisional_invoices')
    ,path('invstore_invoice_update', views.invstore_invoice_update, name='invstore_invoice_update')
    ,path('invstore_invoice_accept', views.invstore_invoice_accept, name='invstore_invoice_accept')
    
    
    #penman
    ,path('penman_list_events', views.penman_list_events, name='penman_list_events')
    ,path('penman_delete_events', views.penman_delete_events, name='penman_delete_events')        
    #paperhouse
    ,path('paperhouse_list_invoice', views.paperhouse_list_invoice, name='paperhouse_list_invoice')    
    ,path('paperhouse_delete_invoice', views.paperhouse_delete_invoice, name='paperhouse_delete_invoice')    
    ,path('tsp_list_invoice', views.tsp_list_invoice, name='tsp_list_invoice')
    
    #striker
    ,path('striker_list_responces', views.striker_list_responces, name='striker_list_responces')
    ,path('striker_delete_responces', views.striker_delete_responces, name='striker_delete_responces')
    
    #,path('swagger-docs/', schema_view)
    #,path('docs/', include_docs_urls(title='TSP Billing'))
    ]



#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
