import os
import sys
import json
import mimetypes
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from tokenleaderclient.client.client import Client 
from micros2client.client import MSClient
from linkinvclient.client import LIClient
from django.views.generic.edit import FormView
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
#File Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from werkzeug.utils import secure_filename
from dashapp.tokenleader import tllogin


 

def list_divinvoices(request):
    if request.method == 'GET': 
        #if 'uname' in request.session:
        #    del request.session['uname']
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient) 
        list_invoices = invClient.display('all')  
        template_data = {"list_divinvoices": list_invoices } 
        result = render(request, 'home.html', template_data)        
        return result
 
## Deleting All/Invoice Number invoices in the System
def invoicediv_delete(request):
   if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient)
        invoicenum = request.POST['invoiceno']          
        invoiceno = int(invoicenum)
        if invoiceno > 0:
             status = invClient.delete_invoice(invoicenum) 
        else:
             status = invClient.delete_invoice('all') 
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient)
        list_invoices = invClient.display('all')  
        template_data = {"list_divinvoices": list_invoices ,"DELETE_INVOICE_STATUS": status} 
        result = render(request, 'home.html', template_data)   
   else:
       tlclient = tllogin.prep_tlclient_from_session(request)
       invClient = MSClient(tlclient)
       list_invoices = invClient.display('all')  
       template_data = {"list_divinvoices": list_invoices } 
       result = render(request, 'home.html', template_data)      
   return result    
 