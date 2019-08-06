import os
import sys
import json
import mimetypes
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from tokenleaderclient.client.client import Client 
from micros1client.client import MSClient

from xlupload_client.client import xlupload_client

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



def downloadinvoicexlformat(request):
    file_path = '/home/ubuntu/dashboard/dashboard/sample_inv_upload.xlsx'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

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
            xluploadclient = xlupload_client(tlclient)        
            Upload_result = xluploadclient.xlupload(uploaded_file_url)      
            message = json.dumps(Upload_result)
            loaded_message = json.loads(message)
            if isinstance(loaded_message, list):
                fs.delete(fname)
            result = render(request, 'home.html', 
                                { 'uploaded_file_url': uploaded_file_url,
                                 "XL_VIEW_UPLOAD": "TRUE", 
                                 "UPLOAD_STATUS":loaded_message})
            template_data = { "uploaded_file_url" : uploaded_file_url                             
                                 ,"UPLOAD_STATUS" : loaded_message,"UPLOAD_RESULT" : Upload_result}
            result = render(request, 'home.html', template_data) 
        if request.method == 'GET':          
            template_data = {"XL_VIEW_UPLOAD": "TRUE" }  
            result = render(request, 'home.html', template_data) 
    except Exception as exception:
        template_data = {"XL_VIEW_UPLOAD": "TRUE","EXCEPTION" :exception,"EXCEPTION_INFO" : sys.exc_info()[0] }  
        result = render(request, 'home.html', template_data) 
    return result     
## UPDATE Invoice

 