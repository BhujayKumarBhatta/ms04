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
from dashapp.tokenleader.tllogin import validate_active_session


sampleinvoice ={ "state": "","arc": "","billingdateto": "","remarks": "", 
"fullsiteaddress": "","customerid": "","servicetype": "","billingdatefrom": "", 
"speed": "", "division": "","taxname": "","total": 0,"accountno": "","pin": 0, 
"circuitid": "", "invoicedate": "","invoiceno": "","siteid": "","gstno": "", 
"premiseno": "", "city": "","tsp": "","customername": "","slno": 0, 
"premisename": "" ,"billingactivity": "" ,"Action": ""}

def list_invoices(request, invoicenum, mode, admin=None):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)        
        paperclient=clientpaperhouse(tlclient)#               
        list_invoices = paperclient.list_invoices(invoicenum)        
        if invoicenum == 'all' and mode =='read':
            template_name = 'invoice/list_invoices.html'            
        elif admin and invoicenum == 'all' and mode == 'read':
            template_name = 'invoice/list_invoices_admin.html'
        elif invoicenum != 'all' and mode == 'edit':
            template_name = 'invoice/edit_invoice.html'
        elif invoicenum != 'all' and mode == 'read':
            template_name = 'invoice/base_read_invoice.html'
            print(template_name)
        edit_button, action_buttons = _get_all_buttons(request, list_invoices)
        template_data = {"PAPERHOUSE_list_invoices": list_invoices,
                         "edit_button": edit_button, "action_buttons": action_buttons }
        web_page = validate_active_session(request, template_name, template_data)
        return web_page
    
def _get_all_buttons(request, list_invoices):
    role = request.session.get('session_user_details').get('roles')[0]
    current_status = list_invoices[0].get('status')
    edit_button = _get_edit_button(role, current_status)
    action_buttons = _get_action_buttons(current_status)
    return  edit_button, action_buttons
    
        
def _get_edit_button(role, current_status): 
    current_stat_for_tsp_edits = ["InfobahnRecommendedtoTSP", "InfobahnApproved", ]    
    current_stat_for_infob_edits = ["InvoiceCreated", "TSPSubmmitedChange",
                                    "DivisionRecommended", "TSPAcceptedChanges"]
    current_stat_for_mis_edits = ["SentToDivision", "TSPCourierdHardCopy" , "HardCopyRecieved"]
    if ( ( role == 'ITC' or role =='role1') and 
         (current_status in current_stat_for_infob_edits) ):
        edit_button = True
    elif role == 'TSP' and current_status in current_stat_for_tsp_edits:
        edit_button = True
    elif role == 'MIS' and current_status in current_stat_for_mis_edits:
        edit_button = True
    else:
        edit_button = False
    return edit_button

def _get_action_buttons(current_status):
    if current_status == "InvoiceCreated":
        button_list = ["InfobahnRecommendedtoTSP", "SentToDivision", ]
    elif current_status == "InfobahnRecommendedtoTSP":
        button_list = ["TSPAcceptedChanges", "TSPSubmmitedChange", ]
    elif current_status == "TSPAcceptedChanges" or current_status == "TSPSubmmitedChange":
        button_list = ["SentToDivision", ]
    elif current_status == "SentToDivision":
        button_list = ["DivisionRecommended", "DivisonApproved", "OverridenDivision", ]
    elif current_status == "DivisionRecommended":
        button_list = ["InfobahnRecommendedtoTSP", "OverridenDivision"]
    elif current_status == "DivisonApproved" or current_status == "OverridenDivision":
        button_list = ["InfobahnApproved",]
    elif current_status == "InfobahnApproved":
        button_list = ["TSPCourierdHardCopy", ]
    elif current_status == "TSPCourierdHardCopy":
        button_list = ["HardCopyRecieved", ]
    elif current_status == "HardCopyRecieved":
        button_list = ["PaymentMade", ]
    else:
        button_list = None
    return button_list
    
    
        
        
       
    
    
        
        
    
    
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


def tsp_list_invoices(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)        
        paperclient=clientpaperhouse(tlclient)        
        list_invoices = paperclient.list_invoices('all')
        message = json.dumps(list_invoices)
        template_data = {"TSP_list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)        
        return result
    

    
    