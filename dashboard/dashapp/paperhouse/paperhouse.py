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
from dashapp.tokenleader.tllogin import validate_active_session
import itertools


INFOB_roles = ['ITSS', "ITC", "role1", "INFOB", "infob"]
current_stat_for_tsp_edits = ["InfobahnRecommendedtoTSP", "InfobahnApproved" ]    
current_stat_for_infob_edits = ["InvoiceCreated", "TSPSubmmitedChange",
                                "DivisionRecommended", "DivisionApproved", "TSPAcceptedChanges" ]
current_stat_for_mis_edits = ["SentToDivision", "TSPCourierdHardCopy" , "HardCopyRecieved"]
current_stat_for_tsp_edits.extend(current_stat_for_infob_edits)
current_stat_for_tsp_edits.extend(current_stat_for_mis_edits)
status_list = current_stat_for_tsp_edits

sampleinvoice ={ "state": "","arc": "","billingdateto": "","remarks": "", 
"fullsiteaddress": "","customerid": "","servicetype": "","billingdatefrom": "", 
"speed": "", "division": "","taxname": "","total": 0,"accountno": "","pin": 0, 
"circuitid": "", "invoicedate": "","invoiceno": "","siteid": "","gstno": "", 
"premiseno": "", "city": "","tsp": "","customername": "","slno": 0, 
"premisename": "" ,"billingactivity": "" ,"Action": ""}

def list_invoices(request, invoicenum, mode, admin=None):
    list_events = []
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)        
        paperclient=clientpaperhouse(tlclient)#               
        list_invoices = paperclient.list_invoices(invoicenum)        
        if invoicenum == 'all' and mode =='read':
            template_name = 'invoice/list_invoices.html'            
        elif admin and invoicenum == 'all' and mode == 'read':
            template_name = 'invoice/list_invoices_admin.html'
        elif invoicenum != 'all' and mode == 'edit':
            penclient=clientpenman(tlclient)      
            list_events = penclient.list_events(invoicenum)
            template_name = 'invoice/edit_invoice.html'
        elif invoicenum != 'all' and mode == 'read':
            penclient=clientpenman(tlclient)      
            list_events = penclient.list_events(invoicenum)
            print(list_events)
            template_name = 'invoice/base_read_invoice.html'
            print(template_name)
        if list_invoices:
            accept_button, edit_button, action_buttons = _get_all_buttons(request, list_invoices)
        else:
            accept_button, edit_button, action_buttons,  = False, False, []
        template_data = {"PAPERHOUSE_list_invoices": list_invoices,
                         "edit_button": edit_button, "action_buttons": action_buttons,
                         "accept_button": accept_button, "list_events": list_events }
        web_page = validate_active_session(request, template_name, template_data)
        return web_page    
    
    
def draft_list(request, status):    
    tlclient = tllogin.prep_tlclient_from_session(request)        
    paperclient=clientpaperhouse(tlclient)#               
    list_invoices = paperclient.list_invoices('all')
    if status == "all":
        save_as_draft_list  = [ l for l in list_invoices if 
                                l.get('xldata').get('action') == "SaveAsDraft"]
        action_buttons = set([(d['status']) for d in save_as_draft_list])
        template_name = 'invoice/list_drafts.html'
    elif status in status_list:
        action_buttons = _get_action_buttons(status)
        print(action_buttons)
        save_as_draft_list = [l for l in list_invoices if 
                     l.get('xldata').get('action') == "SaveAsDraft" and  l.get('status') == status ]
   
        template_name = 'invoice/post_from_drafts.html'
    else:
#         #TODO: WE HAVE DEBUG WHY THIS IS NOT WORKING
#         save_as_draft_list = [{"xldata": {"invoiceno": "invalid  status filter"},"status": "invalid  status filter"}]
        pass
        action_buttons = []
        save_as_draft_list = []
        template_name = 'invoice/list_drafts.html'
    _remove_key_from_list(action_buttons, "SaveAsDraft")
    template_data = { "PAPERHOUSE_list_invoices": save_as_draft_list,
                      "action_buttons": action_buttons}
    web_page = validate_active_session(request, template_name, template_data)
    return web_page


def _remove_key_from_list(your_list, text_key):
    if your_list and isinstance(your_list, list) and text_key in your_list:
        for  n in range(len(your_list)):
            if your_list[n] == text_key:
                your_list.pop(n)
    elif your_list and isinstance(your_list, set) and text_key in your_list:
        your_list.remove(text_key)
    else:
        print("cant remove key from unknown object type")       
        
    return your_list


    
def _get_all_buttons(request, list_invoices):
    try:
        role = request.session.get('session_user_details').get('roles')[0]
        current_status = list_invoices[0].get('status')
        accept_button, edit_button = _get_edit_button(role, current_status)
        action_buttons = _get_action_buttons(current_status)
    except Exception as e:
        accept_button, edit_button, action_buttons = e, e, e
    return  accept_button, edit_button, action_buttons
    
        
def _get_edit_button(role, current_status): 
    accept_button = False 
    if ( ( role in INFOB_roles) and 
         (current_status in current_stat_for_infob_edits) ):
        edit_button = True
    elif role == 'TSP' and current_status in current_stat_for_tsp_edits:
        edit_button = True
        accept_button = True
    elif role == 'MIS' and current_status in current_stat_for_mis_edits:
        edit_button = True
    else:
        edit_button = False
    return accept_button, edit_button

def _get_action_buttons(current_status):
    if current_status == "InvoiceCreated" or current_status == "TSPSubmmitedChange":
        button_list = ["InfobahnRecommendedtoTSP", "SentToDivision", "SaveAsDraft"]
    elif current_status == "InfobahnRecommendedtoTSP":
        button_list = ["ACCEPT", "CHANGE", "SaveAsDraft",]
    elif current_status == "TSPAcceptedChanges":
        button_list = ["SentToDivision", "SaveAsDraft"]
    elif current_status == "SentToDivision":
        button_list = ["DivisionRecommended", "DivisionApproved", "SaveAsDraft" ]
    elif current_status == "DivisionRecommended":
        button_list = ["InfobahnRecommendedtoTSP", "SentToDivision", "OverridenDivision", "SaveAsDraft"]
    elif current_status == "DivisionApproved" or current_status == "OverridenDivision":
        button_list = ["InfobahnApproved", "SaveAsDraft"]
    elif current_status == "InfobahnApproved":
        button_list = ["TSPCourierdHardCopy", "SaveAsDraft"]
    elif current_status == "TSPCourierdHardCopy":
        button_list = ["HardCopyRecieved", "SaveAsDraft"]
    elif current_status == "HardCopyRecieved":
        button_list = ["PaymentMade", "SaveAsDraft"]
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
    

    
    