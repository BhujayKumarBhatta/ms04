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
        #message = json.dumps(list_invoices)
        list_invoices = json.loads(message)
        template_data = {"list_invoices": list_invoices ,"ACCEPT_RCOM" : accept_recomondation} 
        result = render(request, 'home.html', template_data)        
        return result
    if request.method == 'GET': 
        respond_as_attachment(request)
        #tlclient = tllogin.prep_tlclient_from_session(request)
        #invClient = MSClient(tlclient) 
        #list_invoices = invClient.list_invoices_clo('all','all')  
        #template_data = {"list_invoices": list_invoices } 
        #result = render(request, 'home.html', template_data)        
        #return result

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
        #template_data = {"DELETE_STATUS":"Working Delete","list_invoices": list_invoices,"ISDELETED":"TRUE" } 
        template_data = {"list_invoices": list_invoices } 
        result = render(request, 'home.html', template_data)          
   return result
    
## Navigate to Upload Invoice******
def view_upload(request):
   if request.method == 'GET':          
        template_data = {"VIEW_UPLOAD": "TRUE" }  
        result = render(request, 'home.html', template_data)        
        return result



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
     


def view_update_upload(request):
   if request.method == 'GET':          
        template_data = {"VIEW_UPDATE_UPLOAD": "TRUE" }  
        result = render(request, 'home.html', template_data)        
        return result

#def invoice_Update_upload(request):
#    if request.method == 'POST' and request.FILES['myfile']:
#        myfile = request.FILES['myfile']
#        data = request.FILES['myfile'].read()
#        fs = FileSystemStorage(location = '/tmp/media/',
#                               file_permissions_mode = 0o644)
#        fname = secure_filename(myfile.name)
#        filename = fs.save(fname, myfile)
#        uploaded_file_url = fs.url(filename)
#        #Calling Micrios client to Update to DB
#        tlclient = tllogin.prep_tlclient_from_session(request)
#        ms1Client = MSClient(tlclient)
#        message = ms1Client.update_invoice(uploaded_file_url)
#        message = json.dumps(message)
#        loaded_message = json.loads(message)
#        #if isinstance(loaded_message, list):
#        # fs.delete(fname)
#        template_data = { 'uploaded_file_url': uploaded_file_url,
#                             "VIEW_UPDATE_UPLOAD": "TRUE",
#                             "UPLOAD_UPDATE_STATUS":loaded_message}
#        result = render(request, 'home.html',template_data)
#    if request.method == 'GET':
#        template_data = {"VIEW_UPDATE_UPLOAD": "TRUE" }
#        result = render(request, 'home.html', template_data)
#    return result
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
 
 
def respond_as_attachment(request):
    file_path =  "/home/ubuntu/dashboard/dashboard/sample-invoice-xl.xlsx"
    original_filename = "sample-invoice-xl.xlsx"
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response
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


