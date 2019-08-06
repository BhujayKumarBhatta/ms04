import os
import sys
import json
import mimetypes
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from tokenleaderclient.client.client import Client 


from invstore_client.client import invstore_client


from linkinvclient.client import LIClient
from django.views.generic.edit import FormView
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
#File Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from werkzeug.utils import secure_filename
from dashapp.tokenleader import tllogin




def list_invoices(request):
    if request.method == 'GET': 
        #if 'uname' in request.session:
        #    del request.session['uname']
        tlclient = tllogin.prep_tlclient_from_session(request)
        invstoreclient = invstore_client(tlclient)
        invoicenum = request.POST['invoiceno']         
        list_invoices = invstoreclient.list_invoice_byinvnum(invoicenum)        
        message = json.dumps(list_invoices)
        template_data = {"invstore_list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)        
        return result
    
def list_invoice_bycurrent_lastorder(request):
    if request.method == 'GET': 
        #if 'uname' in request.session:
        #    del request.session['uname']
        tlclient = tllogin.prep_tlclient_from_session(request)
    
        invstoreclient = invstore_client(tlclient)
        fieldname = request.POST['fieldname']
        fieldvalue = request.POST['fieldvalue']         
        list_invoices = invstoreclient.list_invoice_bycurrent_lastorder(fieldname, fieldvalue)(invoicenum)        
        message = json.dumps(list_invoices)
        template_data = {"invstore_list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)        
        return result  

def list_invoice_byfield(request):
    if request.method == 'GET': 
        #if 'uname' in request.session:
        #    del request.session['uname']
        tlclient = tllogin.prep_tlclient_from_session(request)    
        invstoreclient = invstore_client(tlclient)
        fieldname = request.POST['fieldname']
        fieldvalue = request.POST['fieldvalue'] 
        level = request.POST['level']         
        list_invoices = invstoreclient.list_invoice_byfield(fieldname, fieldvalue, level)        
        message = json.dumps(list_invoices)
        template_data = {"invstore_list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)        
        return result 

def invoice_delete(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    invstoreclient = invstore_client(tlclient)
    if request.method == 'POST':
 
        invoicenum = request.POST['invoiceno']          
        invoiceno = int(invoicenum)
        if invoiceno and invoiceno > 0:
            status = invstoreclient.delete_invoice(invoicenum) 
        #else:
        #    status = invstoreclient.delete_invoices('all') 
        #template_data = {"DELETE_STATUS":"Working Delete","list_invoices":
        #list_invoices,"ISDELETED":"TRUE" }         
        list_invoices = invstoreclient.list_invoice_bycurrent_lastorder('all','all')  
        template_data = {"invstore_list_invoices": list_invoices ,"DELETE_INVSTORE_INVOICE_STATUS": status} 
        result = render(request, 'home.html', template_data)   
    else:
        list_invoices = invstoreclient.list_invoice_bycurrent_lastorder('all','all')  
        template_data = {"invstore_list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)
              
    return result       
    
 