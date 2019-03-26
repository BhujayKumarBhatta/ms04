import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from tokenleaderclient.client.client import Client 
from micros1client.client   import MSClient
from linkinvclient.client import LIClient
from django.views.generic.edit import FormView
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
#File Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from werkzeug.utils import secure_filename

from dashapp.tokenleader import tllogin
from dashapp.linkinv import linkinv_views as linkv
from dashapp.tokenleader import tlviews
from dashapp.micros1 import tspinv


def login(request):
    result = tllogin.login(request)
    return result


def list_links(request):
    result = linkv.list_links(request)
    return result


def list_org(request):
    result = tlviews.list_org(request)
    return result


def list_ou(request):
    result = tlviews.list_ou(request)
    return result


def list_dept(request):
    result = tlviews.list_dept(request)
    return result

def list_role(request):
    result = tlviews.list_role(request)
    return result


def list_users(request):
    result = tlviews.list_users(request)
    return result

<<<<<<< HEAD
## End ****************************************************
## Invoice Module ****************************************************
def invoice(request):
    if request.method == 'GET': 
        #tlclient = prep_tlclient_from_session(request)
        #list_users = tlclient.list_users()
        template_data = {"INVOICE": "TRUE" }  
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_users))
        return result
=======
>>>>>>> 8d538000860fa0de07c1a2e4b1f3ddb5d70371ca

def adduser(request):
    result = tlviews.adduser(request)
    return result


def list_invoices(request):
    result = tspinv.list_invoices(request)
    return result
    
    
<<<<<<< HEAD
def list_links(request):
    if request.method == 'GET': 
        tlclient = prep_tlclient_from_session(request)
        lic = LIClient(tlclient)
        list_links = lic.list_links()
        template_data = {"list_links": list_links.get('message') } 
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_links))
        return result


def list_test(request):
    if request.method == 'GET': 
        _param1 = request.GET['from']
        _param2 = request.GET['name']
        response = 'You are name is :' + _param1 + ' and from :' + _param2
        return HttpResponse(response)   

    
### Manage Invoice Upload #####################
## List All Invoice
def list_invoices(request):
    if request.method == 'GET': 
        tlclient = prep_tlclient_from_session(request)
        invClient = MSClient(tlclient) 
        list_invoices = invClient.list_invoices('all','all')  
        list_invoices = json.dumps(list_invoices)
        new_jsoninvoices = json.loads(list_invoices)
        
        #list_invoices =
        #JSON.parse(JSON.stringify(list_invoices).replace(/\s(?=\w+":)/g, ""))
        

        #new_json = {x.translate({32: None}): y for x, y in
        #list_invoices.items()}
 
        #list_invoices = invClient.list()
        template_data = None
        template_data = {"list_invoices": new_jsoninvoices } 
        result = render(request, 'home.html', template_data)        
        return result

## Navigate to Upload Invoice******
def view_upload(request):
   if request.method == 'GET':          
        template_data = {"VIEW_UPLOAD": "TRUE" }  
        result = render(request, 'home.html', template_data)        
        return result

## Upload Invoice******
=======
>>>>>>> 8d538000860fa0de07c1a2e4b1f3ddb5d70371ca
def invoice_upload(request):
    result = tspinv.invoice_upload(request)    
    return result


def view_upload(request):
    result = tspinv.view_upload(request)
    return reault


def list_test(request):
    result = linkv.list_test(request)  


