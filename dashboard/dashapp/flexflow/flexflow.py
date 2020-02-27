import os
import sys
import json
from django.http import HttpResponse, Http404
from django.core.files.storage import FileSystemStorage
from werkzeug.utils import secure_filename
from dashapp.tokenleader.tllogin import validate_active_session, validate_token_n_session
from dashapp.tokenleader import tllogin
from clientflexflow.client import clientflexflow



@validate_token_n_session()
def xl_upload(request, wfdoctype):
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
            xluploadclient = clientflexflow(tlclient)        
            Upload_result = xluploadclient.upload_xl(wfdoctype, uploaded_file_url)
            request_id = None
            exec_stat = None
            if Upload_result and isinstance(Upload_result, list):
                request_id = Upload_result.get("request_id")              
                message = json.dumps(Upload_result)
                loaded_message = json.loads(message)
            if isinstance(Upload_result, list):
                fs.delete(fname)          
                #exec_stat = _get_execstat_by_reqid(tlclient, request_id)
            
            template_data = { "XL_uploaded_file_url" : uploaded_file_url,                             
                              "XL_VIEW_UPLOAD" : Upload_result,
                              "XL_UPLOAD_RESULT" : Upload_result,
                              "EXEC_STAT": 'exec_stat'}
    except Exception as exception:
        template_data = {"XL_VIEW_UPLOAD": "TRUE","EXCEPTION" :exception,"EXCEPTION_INFO" : sys.exc_info()[0] }
    web_page = validate_active_session(request, template_name, template_data)
    return web_page     


def download_invoicexlformat(request):
    xl_data_path = os.path.join(os.path.dirname(__file__),
                               os.pardir, 'static', 'xlformat')
    xl_file_path = os.path.join(xl_data_path, 'sample_inv_upload_v2.xlsx')
    print(xl_file_path) 
    if os.path.exists(xl_file_path):
        with open(xl_file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(xl_file_path)
            return response
    raise Http404



@validate_token_n_session()
def add_wfmobj(request, objname):
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient) 
    objfields = flexc.get_wfmobj_keys(objname)
    doctypes = flexc.list_wfmasterObj('Doctype')
    wfstatus_list = flexc.list_wfmasterObj('Wfstatus')
    result = None       
    if request.method == 'POST':
        post_data = {}
        for objfield in objfields:
            objvalue = request.POST.get(objfield)
            if  objfield == "associated_doctype":
                objvalue = {"name": request.POST.get(objfield)}
            if  objfield in  ["permitted_to_roles", "status_needed_edit"] :
                objvalue = request.POST.get(objfield).split(',')
            post_data.update({objfield: objvalue})
        result = flexc.add_wfmasterObj(objname, [post_data])
    template_data = {"objname": objname,
                     "objfields": objfields,
                     "doctypes": doctypes,
                     "wfstatus_list": wfstatus_list,
                     "result": result}
    template_name =  "admin_pages/add_wfmobj.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page


@validate_token_n_session()
def list_wfmobj(request, objname):
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient) 
    objfields = flexc.get_wfmobj_keys(objname)
    object_list = flexc.list_wfmasterObj(objname)        
    if request.method == 'POST':
        post_data = {}
        for objfield in objfields:
            objvalue = request.POST.get(objfield)
            if  objvalue:
                post_data.update({objfield: objvalue})
        object_list = flexc.add_wfmasterObj(objname, [post_data])
    template_data = {"objname": objname,
                     "objfields": objfields,
                     "object_list": object_list,}
    template_name =  "admin_pages/general_list.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page


@validate_token_n_session()
def update_wfmobj(request, objname, filter_by_name):
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient)
    objfields = flexc.get_wfmobj_keys(objname)
    doctypes = flexc.list_wfmasterObj('Doctype')
    wfstatus_list = flexc.list_wfmasterObj('Wfstatus')
    result = None 
    search_filter = {"name": filter_by_name}
    object_detail = flexc.list_wfmasterObj_by_key_val(objname, 'name', filter_by_name)
    for k, v in object_detail.items():
        if k == "associated_doctype":
            adt = {k: v.get("name")}
            object_detail.update(adt)
        if k in  ["permitted_to_roles", "status_needed_edit"]:
            strv = ','.join(v)
            object_detail.update({k: strv})
    if request.method == 'POST':
        post_data = {}
        for objfield in objfields:
            objvalue = request.POST.get(objfield)
            if  objvalue:
                post_data.update({objfield: objvalue})
            if objfield == "associated_doctype":
                post_data.update( {objfield: {"name": objvalue}})
        input_data = {"search_filter": search_filter,
                      "update_data_dict": post_data}
        result = flexc.update_wfmasterObj(objname, input_data)
    template_data = {"objname": objname,
                     "objfields": objfields,
                     "doctypes": doctypes,
                     "wfstatus_list": wfstatus_list,
                     "object_detail": object_detail,                    
                     "result": result,}
    template_name =  "admin_pages/general_edit.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page


@validate_token_n_session()
def delete_wfmobj(request, objname, filter_by_name):
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient)
    objfields = flexc.get_wfmobj_keys(objname)
    object_list = flexc.list_wfmasterObj(objname)         
    result = flexc.delete_wfmasterObj_by_name(objname, filter_by_name)
    object_list = flexc.list_wfmasterObj(objname) 
    template_data = {"objname": objname,
                     "objfields": objfields,
                     "object_list": object_list,                    
                     "result": result,}
    template_name =  "admin_pages/general_list.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page
