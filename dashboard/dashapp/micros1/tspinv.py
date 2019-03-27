import os
import json
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




def list_invoices(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient) 
        list_invoices = invClient.list_invoices_clo('all','all')  
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
        message = ms1Client.upload_xl(uploaded_file_url)      
        message = json.dumps(message)
        loaded_message = json.loads(message)
        if isinstance(loaded_message, list):
            fs.delete(fname)
        result = render(request, 'home.html', 
                            { 'uploaded_file_url': uploaded_file_url,
                             "VIEW_UPLOAD": "TRUE", 
                             "UPLOAD_STATUS":loaded_message})
    if request.method == 'GET':          
        template_data = {"VIEW_UPLOAD": "TRUE" }  
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
def invoice_Update_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']        
        fs = FileSystemStorage(location = '/tmp/media/',file_permissions_mode =  0o644)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        tlclient = tllogin.prep_tlclient_from_session(request)
        ms1Client = MSClient(tlclient)        
        message = ms1Client.update_invoice(uploaded_file_url)      
        message = json.dumps(message)
        #loaded_message = json.loads(message)# Only gives json Object str
        

        template_data = { 'uploaded_file_url': uploaded_file_url,
                              'VIEW_UPDATE_UPLOAD': "TRUE", 
                              'UPLOAD_UPDATE_STATUS':message}
        result = render(request, 'home.html',template_data)
        return result
    if request.method == 'GET':          
        template_data = {"VIEW_UPDATE_UPLOAD": "from view upload" }  
        result = render(request, 'home.html', template_data)   
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
