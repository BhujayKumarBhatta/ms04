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
from clientpenman.client import clientpenman 

from linkinvclient.client import LIClient
from django.views.generic.edit import FormView
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
#File Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from werkzeug.utils import secure_filename
from dashapp.tokenleader import tllogin
from django.db.transaction import non_atomic_requests
from django.contrib.admin.models import CHANGE


sampleinvoice = { "state": "","arc": "","billingdateto": "","remarks": "", 
"fullsiteaddress": "","customerid": "","servicetype": "","billingdatefrom": "", 
"speed": "", "division": "","taxname": "","total": 0,"accountno": "","pin": 0, 
"circuitid": "", "invoicedate": "","invoiceno": "","siteid": "","gstno": "", 
"premiseno": "", "city": "","tsp": "","customername": "","slno": 0, 
"premisename": "" ,"billingactivity": "" ,"Action": ""}

def list_events(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)        
        penclient=clientpenman(tlclient)
        request.POST.get('invoiceno', '')
        invoicenum = request.POST.get('invoiceno', '')
        if invoicenum:         
            list_events = penclient.list_events(invoicenum)        
        else:
            list_events = penclient.list_events('all')
        #message = json.dumps(list_events)
        template_data = {"PENMAN_list_invoices": list_events } 
        result = render(request, 'home.html', template_data)        
        return result
    
    
def delete_events(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    penclient=clientpenman(tlclient)
    if request.method == 'POST':

        invoicenum = request.POST['invoiceno']          
        invoiceno = int(invoicenum)
        if invoiceno and invoiceno > 0:
            status = penclient.delete_events(invoicenum)        
        else:
            status = penclient.delete_events('all') 
        list_events = penclient.list_events('all')  
        template_data = {"PENMAN_list_invoices": list_events ,"DEL_PEN_EVNT_STATUS": status} 
        result = render(request, 'home.html', template_data)   
    else:        
        list_events = penclient.list_events('all')  
        template_data = {"PENMAN_list_invoices": list_events } 
        result = render(request, 'home.html', template_data)      
    return result    
    