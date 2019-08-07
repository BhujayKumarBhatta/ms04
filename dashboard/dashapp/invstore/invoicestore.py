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
        request.POST.get('invoiceno', '')
        invoicenum = request.POST.get('invoiceno', '')
        if invoicenum:         
            list_invoices = invstoreclient.list_invoice_byinvnum(invoicenum)        
        else:
            list_invoices = invstoreclient.list_invoice_byinvnum('all')
        message = json.dumps(list_invoices)
        template_data = {"invstore_list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)        
        return result
    
def list_divinvoices(request):
    if request.method == 'GET': 
        #if 'uname' in request.session:
        #    del request.session['uname']
        tlclient = tllogin.prep_tlclient_from_session(request)
        invstoreclient = invstore_client(tlclient)
        request.POST.get('invoiceno', '')
        invoicenum = request.POST.get('invoiceno', '')
        
        if invoicenum:         
            list_invoices = invstoreclient.list_invoice_byinvnum(invoicenum)        
        else:
            list_invoices = invstoreclient.list_invoice_byinvnum('all')
        message = json.dumps(list_invoices)
        template_data = {"invstore_list_divinvoices": list_invoices } 
        result = render(request, 'home.html', template_data)        
        return result
        
    
def list_invoice_bycurrent_lastorder(request):
    if request.method == 'GET': 
        #if 'uname' in request.session:
        #    del request.session['uname']
        tlclient = tllogin.prep_tlclient_from_session(request)
    
        invstoreclient = invstore_client(tlclient)
        fieldname = request.GET['fieldname']
        fieldvalue = request.GET['fieldvalue']         
        list_invoices = invstoreclient.list_invoice_bycurrent_lastorder(fieldname, fieldvalue)        
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
        fieldname = request.GET['fieldname']
        fieldvalue = request.GET['fieldvalue'] 
        level = request.GET['level']         
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
        else:
            status = invstoreclient.delete_invoice('all') 
        #template_data = {"DELETE_STATUS":"Working Delete","list_invoices":
        #list_invoices,"ISDELETED":"TRUE" }         
        list_invoices = invstoreclient.list_invoice_byinvnum('all')  
        template_data = {"invstore_list_invoices": list_invoices ,"DELETE_INVSTORE_INVOICE_STATUS": status} 
        result = render(request, 'home.html', template_data)   
    else:
        list_invoices = invstoreclient.list_invoice_byinvnum('all')  
        template_data = {"invstore_list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)
              
    return result       
    
def list_stage1responces(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        invstoreclient = invstore_client(tlclient)
        list_responces = invstoreclient.list_stage1responces()
        
        template_data = {"STAGE1RESPONCES": "TRUE" ,"invstore_list_stage1responces": list_responces } 
        result = render(request, 'home.html', template_data)        
        return result

    
def delete_stage1responces(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    invstoreclient = invstore_client(tlclient)
    if request.method == 'POST':       
        status = invstoreclient.delete_stage1responces()
        template_data = {"STAGE1RESPONCES": "TRUE" , "DELETE_STAGE1RESPONCES_STATUS": status} 
        result = render(request, 'home.html', template_data)   

    list_responces = invstoreclient.list_stage1responces()    
    template_data = {"STAGE1RESPONCES": "TRUE" ,"invstore_list_stage1responces": list_responces } 
    result = render(request, 'home.html', template_data)
              
    return result     
        
 
 