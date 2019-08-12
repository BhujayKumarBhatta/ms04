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
from django.db.transaction import non_atomic_requests


sampleinvoice ={ "state": "","arc": "","billingdateto": "","remarks": "", 
"fullsiteaddress": "","customerid": "","servicetype": "","billingdatefrom": "", 
"speed": "", "division": "","taxname": "","total": 0,"accountno": "","pin": 0, 
"circuitid": "", "invoicedate": "","invoiceno": "","siteid": "","gstno": "", 
"premiseno": "", "city": "","tsp": "","customername": "","slno": 0, 
"premisename": "" ,"billingactivity": "" ,"action": ""}

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

  
def invoice_approve(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    invstoreclient = invstore_client(tlclient) 
    ApproveInvoice = 'Exception'
    listdata =[]
    try:
        if request.method == 'POST':
            invnum = request.POST['invoiceno']
            if invnum == 'all':                
                list_invoices = invstoreclient.list_invoice_byinvnum('all')                  
                for hstlist in list_invoices: 
                    for Inv in hstlist['history_list']:
                        dictstruct = {'action': 'approve', 'invoiceno': '0'}
                        dictstruct['invoiceno'] = Inv['xldata']['invoiceno']            
                        listdata.append(dictstruct) 
            else:
                dictstruct = {'action': 'approve', 'invoiceno': '0'}
                dictstruct['invoiceno'] = request.POST['invoiceno']            
                listdata.append(dictstruct) 
                list_invoices = invstoreclient.list_invoice_byinvnum('all')
            list_invoices = invstoreclient.list_invoice_byinvnum('all')            
            invapprove_result = invstoreclient.infobhan_review(listdata)
            template_data = {"invstore_list_divinvoices": list_invoices ,"APPROVE_INVSTORE_INVOICE_STATUS": invapprove_result} 
            result = render(request, 'home.html', template_data)        
        else:
            result = render(request, 'home.html')
    except Exception as exception:
        list_invoices = invstoreclient.list_invoice_byinvnum('all') 
        template_data = {"invstore_list_divinvoices": list_invoices ,"APPROVE_INVSTORE_INVOICE_STATUS": exception} 
        result = render(request, 'home.html', template_data)
    return result 


def invoice_reject(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    invstoreclient = invstore_client(tlclient) 
    ApproveInvoice = 'Exception'
    listdata =[]
    try:
        if request.method == 'POST': 
            invnum = request.POST['invoiceno']
            dictstruct = {'action': 'reject', 'invoiceno': '0'}
            if invnum == 'all':                
                list_invoices = invstoreclient.list_invoice_byinvnum('all')                  
                for hstlist in list_invoices: 
                    for Inv in hstlist['history_list']:
                        dictstruct = {'action': 'reject', 'invoiceno': '0'}
                        dictstruct['invoiceno'] = Inv['xldata']['invoiceno']            
                        listdata.append(dictstruct) 
            else:
                dictstruct = {'action': 'reject', 'invoiceno': '0'}
                dictstruct['invoiceno'] = request.POST['invoiceno']            
                listdata.append(dictstruct) 
                list_invoices = invstoreclient.list_invoice_byinvnum('all') 
             
            invreject_result = invstoreclient.infobhan_review(listdata)
            ##Loading All invoice
            list_invoices = invstoreclient.list_invoice_byinvnum('all')          
            template_data = {"invstore_list_divinvoices": list_invoices ,"REJECT_INVSTORE_INVOICE_STATUS": invreject_result} 
            result = render(request, 'home.html', template_data)        
        else:
            result = render(request, 'home.html')
    except Exception as exception:
        
         ##Loading All invoice
        list_invoices = invstoreclient.list_invoice_byinvnum('all') 
        template_data = {"invstore_list_divinvoices": list_invoices ,"REJECT_INVSTORE_INVOICE_STATUS": exception} 
        result = render(request, 'home.html', template_data)
    return result 
   
    
def invoice_rcommendations(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    invstoreclient = invstore_client(tlclient)
    list_invoices = invstoreclient.list_invoice_byinvnum('all')
    RECOM_invoicelist = []
    TESTDATA = []
    if request.method == 'POST': 
        #all fields will tail with slno
        #RECOM_invoicelist.append(request.POST)
        
        for hstlist in list_invoices: 
            for Inv in hstlist['history_list']:
                slno = Inv['xldata']['slno']
                #slno = slno.strip()
                #RECOM_invoicelist.append('======================')
                #RECOM_invoicelist.append(Inv['xldata'])
                if ('invoiceno'+'_'+ str(slno)) in request.POST and Inv['status'] == 'initialUpload' :                 
                    #RECOM_invoicelist.append(Inv['xldata']['invoiceno'])
                    #id = ('invoiceno'+'_'+ str(slno))
                    #RECOM_invoicelist.append(request.POST['invoiceno_8'])
                    
                    #RECOM_invoicelist.append(request.POST['taxname'+'_'+ str(slno)])
                    TESTDATA.append(request.POST['invoiceno'+'_'+ str(slno)])
                    if (Inv['xldata']['invoiceno'] == request.POST['invoiceno'+'_'+ str(slno)]
                        
                        and (Inv['xldata']['speed'] != request.POST['speed'+'_'+ str(slno)]
                        or   Inv['xldata']['taxname'] != request.POST['taxname'+'_'+ str(slno)]
                        or   Inv['xldata']['customername'] != request.POST['customername'+'_'+ str(slno)])):
                        Recom_Invocie = Inv['xldata'].copy()                        

                        Recom_Invocie['invoiceno'] = request.POST['invoiceno'+'_'+ str(slno)]
                        Recom_Invocie['taxname'] = request.POST['taxname'+'_'+ str(slno)]
                        Recom_Invocie['customername'] = request.POST['customername'+'_'+ str(slno)]
                        Recom_Invocie['state'] = request.POST['state'+'_'+ str(slno)]
                        #Recom_Invocie['arc'] = request.POST['arc'+'_'+ str(slno)]
                        Recom_Invocie['billingdateto'] = request.POST['billingdateto'+'_'+ str(slno)]
                        Recom_Invocie['remarks'] = request.POST['remarks'+'_'+ str(slno)]
                        #Recom_Invocie['customerid'] = request.POST['customerid'+'_'+ str(slno)]
                        Recom_Invocie['billingdatefrom'] = request.POST['billingdatefrom'+'_'+ str(slno)]
                         
                        Recom_Invocie['servicetype'] = request.POST['servicetype'+'_'+ str(slno)]
                        #Recom_Invocie['pin'] = request.POST['pin'+'_'+ str(slno)]
                        #Recom_Invocie['accountno'] = request.POST['accountno'+'_'+ str(slno)]
                        #Recom_Invocie['slno'] = request.POST['slno'+'_'+ str(slno)]
                        #Recom_Invocie['siteid'] = request.POST['siteid'+'_'+ str(slno)]
                        Recom_Invocie['gstno'] = request.POST['gstno'+'_'+ str(slno)]
                        #Recom_Invocie['gstno'] = request.POST['gstno'+'_'+ str(slno)]
                        #Recom_Invocie['gstno'] = request.POST['gstno'+'_'+ str(slno)]
                        #Recom_Invocie['fullsiteaddress'] = request.POST['fullsiteaddress'+'_'+ str(slno)]
                        #Recom_Invocie['total'] = request.POST['total'+'_'+ str(slno)]
                        Recom_Invocie['division'] = request.POST['division'+'_'+ str(slno)]
                        Recom_Invocie['invoicedate'] = request.POST['invoicedate'+'_'+ str(slno)]
                        #Recom_Invocie['billingactivity'] = request.POST['billingactivity'+'_'+ str(slno)]
                        Recom_Invocie['city'] = request.POST['city'+'_'+ str(slno)]
                        Recom_Invocie['customername'] = request.POST['customername'+'_'+ str(slno)]
                        Recom_Invocie['premisename'] = request.POST['premisename'+'_'+ str(slno)]
                        #Recom_Invocie['tsp'] = request.POST['tsp'+'_'+ str(slno)]                        
                        Recom_Invocie['premiseno'] = request.POST['premiseno'+'_'+ str(slno)]
                        Recom_Invocie['circuitid'] = request.POST['circuitid'+'_'+ str(slno)]
                        Recom_Invocie['action'] = 'recommend'
                        RECOM_invoicelist.append(Recom_Invocie)        
                        #RECOM_invoicelist.append(request.POST['speed'+'_'+ str(slno)])
                        #RECOM_invoicelist.append(request.POST['customername'+'_'+ str(slno)])
        invrcom_result = None
        #removing duplicate 
        RECOM_invoicelist_noduplicates = [i for n, i in enumerate(RECOM_invoicelist) if i not in RECOM_invoicelist[n + 1:]]
            #RECOM_invoicelist.append(request.POST['taxname'+'_'+ str(slno)]) 
        if len(RECOM_invoicelist) > 0:
            invrcom_result = invstoreclient.infobhan_review(RECOM_invoicelist_noduplicates)
        message = json.dumps(list_invoices)
        template_data = {"invstore_list_invoices_RCOM": list_invoices,"RECOM_invoicelist": RECOM_invoicelist_noduplicates ,"TESTDATA":TESTDATA, 'RCOM_STATUS' :invrcom_result} 
        result = render(request, 'home.html', template_data)        
        
    elif request.method == 'GET': 
        message = json.dumps(list_invoices)
        template_data = {"invstore_list_invoices_RCOM": list_invoices } 
        result = render(request, 'home.html', template_data)        
    
    return result
    
 
 
def list_divisional_invoices(request):
    if request.method == 'GET':
        tlclient = tllogin.prep_tlclient_from_session(request)
        invstoreclient = invstore_client(tlclient)
        list_invoices = invstoreclient.list_invoice_byinvnum('all')
        message = json.dumps(list_invoices)
        template_data = {"invstore_DIVSION_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)        
        return result
 