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
from clientstriker.client import clientstriker

from linkinvclient.client import LIClient
from django.views.generic.edit import FormView
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
#File Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from werkzeug.utils import secure_filename
from dashapp.tokenleader import tllogin
from dashapp.tokenleader.tllogin import validate_active_session




def download_invoicexlformat(request):
    xl_data_path = os.path.join(os.path.dirname(__file__),
                               os.pardir, 'static', 'xlformat')
    xl_file_path = os.path.join(xl_data_path, 'sample_inv_upload.xlsx')
    print(xl_file_path) 
    if os.path.exists(xl_file_path):
        with open(xl_file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(xl_file_path)
            return response
    raise Http404

def _get_execstat_by_reqid(tlclient, request_id):
    strikerclient=clientstriker(tlclient)
    list_responces = strikerclient.list_responses()
    print(list_responces)
    filtered_list = []
    for l in list_responces:
        rid = l.get('wfcdict').get('request_id')
#         print(rid, request_id)
        if rid == request_id:
            filtered_list.append(l)
    print(filtered_list)           
    return filtered_list

def invoice_upload(request):
    template_name = "invoice/xlupload_invoice.html"
    try:
        if request.method == 'GET':
            template_name = "invoice/xlupload_invoice.html"       
            template_data = {"XL_VIEW_UPLOAD": "TRUE" }  

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
            request_id = Upload_result.get("request_id")    
            message = json.dumps(Upload_result)
            loaded_message = json.loads(message)
            if isinstance(loaded_message, list):
                fs.delete(fname)          
            exec_stat = _get_execstat_by_reqid(tlclient, request_id)
            template_data = { "XL_uploaded_file_url" : uploaded_file_url,                             
                              "XL_VIEW_UPLOAD" : loaded_message,
                              "XL_UPLOAD_RESULT" : Upload_result,
                              "EXEC_STAT": exec_stat}

         
    except Exception as exception:
        template_data = {"XL_VIEW_UPLOAD": "TRUE","EXCEPTION" :exception,"EXCEPTION_INFO" : sys.exc_info()[0] }  

    web_page = validate_active_session(request, template_name, template_data)
    return web_page     
## UPDATE Invoice

 