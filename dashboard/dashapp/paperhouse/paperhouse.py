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
from clientpaperhouse.client import clientpaperhouse

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


sampleinvoice ={ "state": "","arc": "","billingdateto": "","remarks": "", 
"fullsiteaddress": "","customerid": "","servicetype": "","billingdatefrom": "", 
"speed": "", "division": "","taxname": "","total": 0,"accountno": "","pin": 0, 
"circuitid": "", "invoicedate": "","invoiceno": "","siteid": "","gstno": "", 
"premiseno": "", "city": "","tsp": "","customername": "","slno": 0, 
"premisename": "" ,"billingactivity": "" ,"Action": ""}

def list_invoices(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)        
        paperclient=clientpaperhouse(tlclient)
        request.POST.get('invoiceno', '')
        invoicenum = request.POST.get('invoiceno', '')
        if invoicenum:         
            list_invoices = paperclient.list_invoices(invoicenum)        
        else:
            list_invoices = paperclient.list_invoices('all')
        message = json.dumps(list_invoices)
        template_data = {"PAPERHOUSE_list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)        
        return result
    
    
def delete_invoices(request):
   if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        paperclient = clientpaperhouse(tlclient)
        invoicenum = request.POST['invoiceno']          
        invoiceno = int(invoicenum)
        if invoiceno and invoiceno > 0:
             status = paperclient.delete_invoices(invoicenum) 
        else:
             status = paperclient.delete_invoices('all') 
        #template_data = {"DELETE_STATUS":"Working Delete","list_invoices":
        #list_invoices,"ISDELETED":"TRUE" }         
        list_invoices = paperclient.list_invoices('all')  
        template_data = {"PAPERHOUSE_list_invoices": list_invoices ,"DEL_PAPER_INV_STATUS": status} 
        result = render(request, 'home.html', template_data)   
   else:
       tlclient = tllogin.prep_tlclient_from_session(request)
       MC1Client = paperclient(tlclient)
       list_invoices = MC1Client.list_invoices('all')    
       template_data = {"PAPERHOUSE_list_invoices": list_invoices } 
       result = render(request, 'home.html', template_data)      
   return result    




    
    