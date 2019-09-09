import os
import sys
import json
import mimetypes
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from tokenleaderclient.client.client import Client
from clientstriker.client import clientstriker
from linkinvclient.client import LIClient
from django.views.generic.edit import FormView
from django.urls import reverse_lazy#File Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from werkzeug.utils import secure_filename
from dashapp.tokenleader import tllogin
from django.db.transaction import non_atomic_requests
from django.contrib.admin.models import CHANGE

# ======TSP=====
# CREATE
# CHANGE
# ACCEPT
# TSPCourierdHardCopy
# =====INFOBAHN=====
# InfobahnRecommendedtoTSP
# SentToDivision
# InfobahnApproved
# OverridenDivision
# ======DIVISION=====
# DivisionRecommended
# DivisionApproved
# HardCopyRecieved
# PaymentMade


sampleinvoice = { "state": "","arc": "","billingdateto": "","remarks": "", 
"fullsiteaddress": "","customerid": "","servicetype": "","billingdatefrom": "", 
"speed": "", "division": "","taxname": "","total": 0,"accountno": "","pin": 0, 
"circuitid": "", "invoicedate": "","invoiceno": "","siteid": "","gstno": "", 
"premiseno": "", "city": "","tsp": "","customername": "","slno": 0, 
"premisename": "" ,"billingactivity": "" ,"Action": ""}

def list_events(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)        
        strikerclient=clientstriker(tlclient)
        list_events = strikerclient.list_events()            
        template_data = {"STRK_list_events": list_events } 
        result = render(request, 'home.html', template_data)        
        return result
    
def list_responces(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)        
        strikerclient=clientstriker(tlclient)
        list_responces = strikerclient.list_responses()
                    
        template_data = {"STRK_list_responces": list_responces } 
        result = render(request, 'home.html', template_data)        
        return result
           
    
def delete_responces(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    strikerclient=clientstriker(tlclient)
    if request.method == 'POST':
        #invoicenum = request.POST['invoiceno']          
        #invoiceno = int(invoicenum)
        status = strikerclient.delete_response() 
        list_responces = strikerclient.list_responses()
        template_data = {"STRK_list_responces": list_responces ,"DEL_STRK_STATUS": status} 
        result = render(request, 'home.html', template_data)   
    else:        
        list_responces = strikerclient.list_responses()  
        template_data = {"STRK_list_responces": list_events } 
        result = render(request, 'home.html', template_data)      
    return result    


def customer_action(request):
    try:
        tlclient = tllogin.prep_tlclient_from_session(request)
        strikerclient=clientstriker(tlclient)
        if request.method == 'POST':
            METHOD = "POST" 
            #TEST DATA ...Data needs to be read from the form post
            sampledata = { "state": "xxx","arc": "xxx","billingdateto": "", "remarks": "", "fullsiteaddress": "", "customerid": "", 
                   "servicetype": "", "billingdatefrom": "", "speed": "", "division": "", "taxname": "", "total": "", 
                   "accountno": "", "pin": "", "circuitid": "", "invoicedate": "", "invoiceno": "1", "siteid": "", "gstno": "", 
                   "premiseno": "", "city": "", "tsp": "", "customername": "", "slno": "",  "premisename": ""
            ,"Action" : "" }
            dictinvoice = dict(sampledata)
            CUT_ACTION = ''
            cust_action_result = trigger_action(sampledata,CUT_ACTION,request)
#             if dictinvoice is not None:       
#                 cust_action_result = strikerclient.customer_action(dictinvoice)                    
            create_result_dump = json.dumps(cust_action_result)
            create_result_load = json.loads(create_result_dump)
            template_data = {"METHOD":METHOD, "STRK_CUSTOMER_ACT": "TRUE","EXTRACTED":None,'RESULT' : create_result_load}
            result = render(request, 'home.html',template_data)
        if request.method == 'GET':
            METHOD = "GET"
            #template_data = {"METHOD":METHOD,"VIEW_CREATE_INVOICE":
            #"TRUE",'CREATE_INVOICE_FORM': form }
            result = render(request, 'home.html', {"METHOD":METHOD, "VIEW_CREATE_INVOICE": "TRUE"}) 
    except Exception as exception:
        template_data = {"VIEW_CREATE_INVOICE": "TRUE","EXCEPTION" :exception,"EXCEPTION_INFO" : sys.exc_info()[0]}  
        result = render(request, 'home.html', template_data) 
    return result


def trigger_action(data, action, request):
    sampledata = { "state": "xxx","arc": "xxx","billingdateto": "", "remarks": "", "fullsiteaddress": "", "customerid": "", 
                   "servicetype": "", "billingdatefrom": "", "speed": "", "division": "", "taxname": "", "total": "", 
                   "accountno": "", "pin": "", "circuitid": "", "invoicedate": "", "invoiceno": "1", "siteid": "", "gstno": "", 
                   "premiseno": "", "city": "", "tsp": "", "customername": "", "slno": "",  "premisename": ""
            ,"Action" : "" }
    sampledata['Action'] = action
    dictinvoice = dict(sampledata)
    if dictinvoice is not None:  
        tlclient = tllogin.prep_tlclient_from_session(request)
        strikerclient=clientstriker(tlclient)     
        cust_action_result = strikerclient.customer_action(dictinvoice)                    
        create_result_dump = json.dumps(cust_action_result)
        create_result_load = json.loads(create_result_dump)
        return cust_action_result       
                
def tsp_action(request):
    try:
        tlclient = tllogin.prep_tlclient_from_session(request)
        strikerclient=clientstriker(tlclient)
        if request.method == 'POST':
            METHOD = "POST" 
            #TEST DATA ...Data needs to be read from the form post
            dictinvoice = dict({ "state": "","arc": "","billingdateto": "", "remarks": "", "fullsiteaddress": "", "customerid": "", 
                   "servicetype": "", "billingdatefrom": "", "speed": "", "division": "", "taxname": "", "total": "", 
                   "accountno": "", "pin": "", "circuitid": "", "invoicedate": "", "invoiceno": "", "siteid": "", "gstno": "", 
                   "premiseno": "", "city": "", "tsp": "", "customername": "", "slno": "",  "premisename": "","action" : "" 
                    })
            if dictinvoice is not None:       
                cust_action_result = strikerclient.tsp_action(dictinvoice)                    
                create_result_dump = json.dumps(cust_action_result)
                create_result_load = json.loads(create_result_dump)
                template_data = {"METHOD":METHOD, "STRK_CUSTOMER_ACT": "TRUE","EXTRACTED":None}
            result = render(request, 'home.html',template_data)
        if request.method == 'GET':
            METHOD = "GET"
            #template_data = {"METHOD":METHOD,"VIEW_CREATE_INVOICE":
            #"TRUE",'CREATE_INVOICE_FORM': form }
            result = render(request, 'home.html', {"METHOD":METHOD, "VIEW_CREATE_INVOICE": "TRUE"}) 
    except Exception as exception:
        template_data = {"VIEW_CREATE_INVOICE": "TRUE","EXCEPTION" :exception,"EXCEPTION_INFO" : sys.exc_info()[0]}  
        result = render(request, 'home.html', template_data) 
    return result
    