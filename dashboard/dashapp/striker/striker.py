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
from dashapp.tokenleader.tllogin import validate_active_session

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
    
def list_exec_status(request, request_id):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)        
        strikerclient=clientstriker(tlclient)
        list_responces = strikerclient.list_responses()
        if request_id != "all":
            filtered_list = []
            for l in list_responces:
                rid = l.get('wfcdict').get('request_id')
                if rid == request_id:
                    filtered_list.append(l)
            list_responces = filtered_list               
        template_data = {"list_exec_status": list_responces } 
        template_name =  'invoice/exec_status.html'        
    web_page = validate_active_session(request, template_name, template_data)
    return web_page
           
    
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

def update_invoice(request, actionrole):
    if request.method == 'POST':
        data = None
        infobahn_roles = ["role1", "INFOBAHN"]
        TSP_roles = ["TSP"]
        MIS_roles = ["MIS"]
        tlclient = tllogin.prep_tlclient_from_session(request)
        strikerclient=clientstriker(tlclient)
        vdata =  _vaidate_data_invoice_update(request)
        if vdata:
            data = [vdata, ]
            if actionrole in infobahn_roles:
                posting_result = strikerclient.customer_action(data)
            elif actionrole in TSP_roles:
                posting_result = strikerclient.tsp_action(data)
            elif actionrole in MIS_roles:
                posting_result = strikerclient.division_action(data)
            else:
                posting_result = ("Failed, User need to have one of "
                                  "role from [role1, INFOBAHN, TSP, MIS]")
        else:
            posting_result = "invalid data or no changes to update invoice"
    template_data = {"update_request": posting_result }
    template_name = "invoice/exec_status.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page

#############data validation before invoice update call ########################################
def _vaidate_data_invoice_update(request):
    rdict = request.POST.copy()
    # remove extra keys which should not be part of xldata comparison
    rdict.pop("csrfmiddlewaretoken")
    prev_status = rdict.pop("status")
    # query dict values are list , convert them as text, 
    #simply reading the will return the last value from the list as per django doc
    nrdict = {}
    for k, v in rdict.items():            
        nrdict[k] = v
    #also pop the last_data key , which is now a text instead of list after the previous step
    # and assign it to a var for later usage         
    last_data = nrdict.pop('last_data')
    #any value in the quey dict is a text hence send it trough myjsoify custom tag and json load here
    last_data = json.loads(last_data)
    print(type(last_data))
    #filter only those keys and values that are not null
    xl_data_wo_blank_values = {}
    for k, v in nrdict.items():
        if v:
            xl_data_wo_blank_values[k] = v
    #There should be at least one field value changed apart Action
    inv_n_action = {"InvoiceNo": xl_data_wo_blank_values.pop("InvoiceNo"),
                    "Action":xl_data_wo_blank_values.pop("Action")}
    print("xl_data_wo_blank_values", xl_data_wo_blank_values)
    #cross check that the values have changed from the last_data
    if xl_data_wo_blank_values:
        values_changed_from_last_time = {}
        for k, v in xl_data_wo_blank_values.items():
            print("last_data", type(last_data))
            if v != last_data.get(k):
                values_changed_from_last_time[k] = v
        values_changed_from_last_time.update(inv_n_action)
        return values_changed_from_last_time
    
#############END data validation before invoice update call ########################################
        
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

###################################

    