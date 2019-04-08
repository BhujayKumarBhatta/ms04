import os
import sys
import json
import mimetypes
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from tokenleaderclient.client.client import Client 
from micros1client.client import MSClient
from linkinvclient.client import LIClient
from django.views.generic.edit import FormView
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
#File Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from werkzeug.utils import secure_filename

from dashapp.tokenleader import tllogin
from dashapp.micros1.invoiceForm import invoiceForm

def list_invoices2(request,invoicnum):
    if request.method == 'POST': 
        #tlclient = tllogin.prep_tlclient_from_session(request)
        #invClient = MSClient(tlclient)
        #list_invoices = invClient.list_invoices_clo('all','all')
        template_data = {"list_invoices": list_invoices ,"POSTING" : "Posting is working ............" + invoicnum} 
        result = render(request, 'home.html', template_data)        
        return result

def list_invoices(request):
    ## AcceptingInvoice
    if request.method == 'POST':         
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient)         
        invoicenum = request.POST['invoicenum']
        my_list = [invoicenum] 
        accept_recomondation = invClient.accept_recom(my_list)
        list_invoices = invClient.list_invoices_clo('all','all')
        message = json.dumps(list_invoices)
        list_invoices = json.loads(message)
        template_data = {"list_invoices": list_invoices ,"ACCEPT_RCOM" : accept_recomondation} 
        result = render(request, 'home.html', template_data)        
        return result
    if request.method == 'GET':          
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient) 
        list_invoices = invClient.list_invoices_clo('all','all')  
        template_data = {"list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)        
        return result

def list_invoice_rcom(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient) 
        list_invoices = invClient.list_invoices_clo('all','all')  
        template_data = {"list_invoices": list_invoices,"IS_RCOM":"TRUE" } 
        result = render(request, 'home.html', template_data)        
        return result
## Deleting All invoices in the System
def invoice_delete(request):
   if request.method == 'GET':          
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient)          
        status = invClient.delete_invoices('all') 
        list_invoices = invClient.list_invoices_clo('all','all')  
        #template_data = {"DELETE_STATUS":"Working Delete","list_invoices":
        #list_invoices,"ISDELETED":"TRUE" }
        template_data = {"list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)          
   return result    
## Navigate to Upload Invoice******
def view_upload(request):
   if request.method == 'GET':          
        template_data = {"VIEW_UPLOAD": "TRUE" }  
        result = render(request, 'home.html', template_data)        
        return result
##CREATE Invoice
def invoice_create(request):
    try:
        #form = invoiceForm()
        if request.method == 'POST': 
            #Calling Micrios client t Upload to DB
            METHOD = "POST"
            extractedInvoice = extractInvoice(request)
            #dictionary to
            #extractInvoice.INVOICE_OBJ.items()
            #Newinvoice == json.dumps(extractedInvoice)
            dictinvoice = dict({ "state": "","arc": "","billingdateto": "", "remarks": "", "fullsiteaddress": "", "customerid": "", 
                   "servicetype": "", "billingdatefrom": "", "speed": "", "division": "", "taxname": "", "total": "", 
                   "accountno": "", "pin": "", "circuitid": "", "invoicedate": "", "invoiceno": "", "siteid": "", "gstno": "", 
                   "premiseno": "", "city": "", "tsp": "", "customername": "", "slno": "",  "premisename": "" 
                    })
            listInvoice = dictinvoice.items()
            if listInvoice is not null:
                tlclient = tllogin.prep_tlclient_from_session(request)
                ms1Client = MSClient(tlclient)        
                Upload_result = ms1Client.create_invoice_list(listInvoice)                    
                create_result_dump = json.dumps(create_result)
                create_result_load = json.loads(message)
                #template_data = {"METHOD":METHOD, "VIEW_CREATE_INVOICE":
                #"TRUE","EXTRACTED":extractedInvoice,"INVOICE_CREATE_RESULT"
                #:create_result_load}
                template_data = {"METHOD":METHOD, "VIEW_CREATE_INVOICE":
                "TRUE","EXTRACTED":listInvoice}
            #result = render(request, 'home.html',{"METHOD":METHOD,
            #"VIEW_CREATE_INVOICE": "TRUE","EXTRACTED":extractedInvoice})
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
##UPLOAD Invoice
def invoice_upload(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            data = request.FILES['myfile'].read()
            fs = FileSystemStorage(location = '/tmp/media/',
                                   file_permissions_mode =  0o644) 
            fname = secure_filename(myfile.name)
            filename = fs.save(fname, myfile)        
            uploaded_file_url = fs.url(filename)

            #Calling Micrios client t Upload to DB
            tlclient = tllogin.prep_tlclient_from_session(request)
            ms1Client = MSClient(tlclient)        
            Upload_result = ms1Client.upload_xl(uploaded_file_url)      
            message = json.dumps(Upload_result)
            loaded_message = json.loads(message)
            if isinstance(loaded_message, list):
                fs.delete(fname)
            result = render(request, 'home.html', 
                                { 'uploaded_file_url': uploaded_file_url,
                                 "VIEW_UPLOAD": "TRUE", 
                                 "UPLOAD_STATUS":loaded_message})
            template_data = { "uploaded_file_url" : uploaded_file_url                             
                                 ,"UPLOAD_STATUS" : message,"UPLOAD_RESULT" : Upload_result}
            result = render(request, 'home.html', template_data) 
        if request.method == 'GET':          
            template_data = {"VIEW_UPLOAD": "TRUE" }  
            result = render(request, 'home.html', template_data) 
    except Exception as exception:
        template_data = {"VIEW_UPLOAD": "TRUE","EXCEPTION" :exception,"EXCEPTION_INFO" : sys.exc_info()[0] }  
        result = render(request, 'home.html', template_data) 
    return result     
## UPDATE Invoice
def view_update_upload(request):
   if request.method == 'GET':          
        template_data = {"VIEW_UPDATE_UPLOAD": "TRUE" }  
        result = render(request, 'home.html', template_data)        
        return result
## UPDATE Invoice
def invoice_update_upload(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage(location = '/tmp/media/',file_permissions_mode =  0o644)
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            tlclient = tllogin.prep_tlclient_from_session(request)
            ms1Client = MSClient(tlclient)        
            Upload_result = ms1Client.update_invoice(uploaded_file_url)      
            message = json.dumps(Upload_result)
            loaded_message = json.loads(message)# Only gives json Object str

            template_data = { "uploadedupdate_file_url" : uploaded_file_url
                             ,"VIEW_UPDATE_UPLOAD" : "TRUE"
                             ,"UPLOAD_UPDATE_STATUS" : message,"UPLOAD_RESULT" : Upload_result}
            result = render(request, 'home.html',template_data)
            return result
        if request.method == 'GET':          
            template_data = {"VIEW_UPDATE_UPLOAD": "from view upload" }  
            result = render(request, 'home.html', template_data)       
    except Exception as exception:
        template_data = {"VIEW_UPDATE_UPLOAD": "from view upload","EXCEPTION" :exception,"EXCEPTION_INFO" : sys.exc_info()[0] }  
        result = render(request, 'home.html', template_data) 
    return result
##RECOMMOND Invoice
def invoice_rcom_upload(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage(location = '/tmp/media/',file_permissions_mode =  0o644)
            filename = fs.save(myfile.name, myfile)
            rcomuploaded_file_url = fs.url(filename)

            tlclient = tllogin.prep_tlclient_from_session(request)
            ms1Client = MSClient(tlclient)        
            Upload_result = ms1Client.recommend_changes_xl(rcomuploaded_file_url)      
            message = json.dumps(Upload_result)
            loaded_message = json.loads(message)# Only gives json Object str

            template_data = { "rcomuploaded_file_url" : rcomuploaded_file_url
                             ,"VIEW_RCOM_UPLOAD" : "TRUE"
                             ,"UPLOAD_RCOM_STATUS" : message,"UPLOAD_RESULT" : Upload_result}
            result = render(request, 'home.html',template_data)
            return result
        if request.method == 'GET':          
            template_data = {"VIEW_RCOM_UPLOAD": "from view upload" }  
            result = render(request, 'home.html', template_data)       
    except Exception as exception:
        template_data = {"VIEW_RCOM_UPLOAD": "from view upload","EXCEPTION" :exception,"EXCEPTION_INFO" : sys.exc_info()[0] }  
        result = render(request, 'home.html', template_data) 
    return result
##APPROVE Invoice
def invoice_approvals(request):
   if request.method == 'GET':  
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient)         
        #invoicenum = request.POST['invoicenum']
        #invoice_list = [invoicenum] 
        #accept_recomondation = invClient.approve_invoices(invoice_list)
        ##Loading All invoice
        list_invoices = invClient.list_invoices_clo('all','all')          
        template_data = {"list_invoices": list_invoices,"APPROVALS":"TRUE" } 
        result = render(request, 'invoice_approvals.html', template_data)          
   return result
##APPROVE Invoice
def invoice_approve(request):
   if request.method == 'POST':  
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient)         
        invoicenum = request.POST['invoicenum']
        invoice_list = [invoicenum] 
        accept_recomondation = invClient.approve_invoices(invoice_list)
        ##Loading All invoice
        list_invoices = invClient.list_invoices_clo('all','all')          
        template_data = {"list_invoices": list_invoices,"APPROVALS":"TRUE" } 
        result = render(request, 'home.html', template_data)          
   return result
## REJECT Invoice
def invoice_reject(request):
   if request.method == 'POST':          
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient) 
        invoicenum = request.POST['invoicenum']
        invoice_list = [invoicenum] 
        status = invClient.reject_invoices() 
        list_invoices = invClient.list_invoices_clo('all','all')  
        template_data = {"list_invoices": list_invoices,"APPROVALS":"TRUE" } 
        result = render(request, 'home.html', template_data)          
   return result


def extractInvoice(request):
    try:
        dictinvoice = dict({ "state": "","arc": "","billingdateto": "", "remarks": "", "fullsiteaddress": "", "customerid": "", 
                             "servicetype": "", "billingdatefrom": "", "speed": "", "division": "", "taxname": "", "total": "", 
                               "accountno": "", "pin": "", "circuitid": "", "invoicedate": "", "invoiceno": "", "siteid": "", "gstno": "", 
                               "premiseno": "", "city": "", "tsp": "", "customername": "", "slno": "",  "premisename": "" 
                            }) 
        #createform = invoiceForm(request.POST)
        if request.method == 'POST':
            #request.POST.get('is_private', False)

            dictinvoice["invoiceno"] = request.POST.get("invoiceno","TEST")  
            dictinvoice["circuitid"] = request.POST.get("circuitid") 
            dictinvoice["division"] = request.POST.get("division") 
            dictinvoice['billingdateto'] = request.POST.get('billingdateto') 
            dictinvoice['remarks'] = request.POST.get('remarks') 
            dictinvoice['fullsiteaddress'] = request.POST.get('fullsiteaddress')
            dictinvoice['customerid'] = request.POST.get('customerid')
            dictinvoice['servicetype'] = request.POST.get('servicetype')
            dictinvoice['billingdatefrom'] = request.POST.get('billingdatefrom')
            dictinvoice['speed'] = request.POST.get('speed')
            dictinvoice['division'] = request.POST.get('division')
            dictinvoice['taxname'] = request.POST.get('taxname')
            dictinvoice['total'] = request.POST.get('total')
            dictinvoice['accountno'] = request.POST.get('accountno')
            dictinvoice['pin'] = request.POST.get('pin')
            dictinvoice['circuitid'] = request.POST.get('circuitid')
            dictinvoice['invoicedate'] = request.POST.get('invoicedate')
            dictinvoice['invoiceno'] = request.POST.get('invoiceno')
            dictinvoice['siteid'] = request.POST.get('siteid')
            dictinvoice['gstno'] = request.POST.get('gstno')
            dictinvoice['premiseno'] = request.POST.get('premiseno')
            dictinvoice['city'] = request.POST.get('city')
            dictinvoice['tsp'] = request.POST.get('tsp')
            dictinvoice['slno'] = request.POST.get('slno')
            dictinvoice['premisename'] = request.POST.get('premisename')
        template_data = {"STATUS": "EXTRACTED","INVOICE_OBJ":dictinvoice}
        result = dictinvoice             
    except Exception as exception:
            template_data = {"STATUS": "There is an error while retriving Object","EXCEPTION" :exception,"EXCEPTION_INFO" : sys.exc_info()[0] }  
            result = template_data 
    return result
 

             
 
 
# 
# 
# ## Upload Invoice******
# def invoice_upload(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         data = request.FILES['myfile'].read()
#         fs = FileSystemStorage(location = '/tmp/media/',
#                                file_permissions_mode =  0o644) 
# #         fs = FileSystemStorage()
# #         fname = (os.path.join('/tmp/media/' , myfile.name))
#         fname = myfile.name
#         filename = fs.save(fname, myfile)
#         
#         uploaded_file_url = fs.url(filename)
# 
#         #Calling Micrios client t Upload to DB
#         tlclient = prep_tlclient_from_session(request)
#         ms1Client = MSClient(tlclient) 
#         #Calling Upload Function
#         message = ms1Client.upload_xl(uploaded_file_url)
# #         message = invClient.upload_xl("/home/ubuntu/dashboard/dashboard" + uploaded_file_url)          
#         message = json.dumps(message)
#         loaded_message = json.loads(message)
#         if isinstance(loaded_message, list):
#             fs.delete(fname)
#             
# 
# 
#         result = render(request, 'home.html', { 'uploaded_file_url': uploaded_file_url,"VIEW_UPLOAD": "TRUE","UPLOAD_STATUS":loaded_message})
#     if request.method == 'GET':          
#         template_data = {"VIEW_UPLOAD": "TRUE" }  
#         result = render(request, 'home.html', template_data) 
#     return result
# 
# 
# ### End Invoice #####################
# 
# 
# #def simple_upload(request):
# #    if request.method == 'POST' and request.FILES['myfile']:
# #        myfile = request.FILES['myfile']
# #        fs = FileSystemStorage()
# #        filename = fs.save(myfile.name, myfile)
# #        uploaded_file_url = fs.url(filename)
# #        return render(request, 'simple_upload.html', {'uploaded_file_url': uploaded_file_url})
# #    return render(request, 'simple_upload.html')





 #{ "state": "","arc": "","billingdateto": "", "remarks": "", "fullsiteaddress": "", "customerid": "","servicetype": "", "billingdatefrom": "", "speed": "", "division": "", "taxname": "", "total": "", "accountno": "", "pin": "", "circuitid": "", "invoicedate": "", "invoiceno": "", "siteid": "", "gstno": "", "premiseno": "", "city": "", "tsp": "", "customername": "", "slno": "",  "premisename": "" }