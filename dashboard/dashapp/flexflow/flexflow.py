import os
import sys
import json
from django.http import HttpResponse, Http404
from django.core.files.storage import FileSystemStorage
from werkzeug.utils import secure_filename
from dashapp.tokenleader.tllogin import validate_active_session, validate_token_n_session
from dashapp.tokenleader import tllogin
from clientflexflow.client import clientflexflow
from django.template.defaultfilters import lower
from pip._internal import req

fields_for_text_to_list_conversion = [
    "need_current_status",
    "permitted_to_roles", 
    "status_needed_edit", 
    "roles_to_view_audit",
    "hide_to_roles",
    "undo_prev_hide_for",
    "wfc_filter_to_roles",
    ]

def _get_fieldnames_from_object(object_detail):
    data_fields = []
    result = object_detail
    if isinstance(object_detail, dict):
        for k, v in object_detail.items():
            if k == "associated_doctype" and isinstance(v, dict):
                adt = {k: v.get("name")}
                object_detail.update(adt)
        if 'doc_data' in object_detail.keys():
            data_fields = object_detail.get('doc_data').keys()
            result = None
    return data_fields, result

def _lower_key_dict(input_dict):
    lower_dict = {}
    for k, v in input_dict.items():
        lower_dict.update({k.lower(): v})
    return lower_dict

def _get_relv_fields_fm_post_using_doc_data_struc(object_detail, request):
    '''pick_relevant_fields_from_post_based_on_doc_data_structure'''
    form_doc_data = {}
    existing_doc_data = object_detail.get('doc_data')
    for objfield in existing_doc_data:
        objvalue = request.POST.get(objfield)
        if  objvalue:
            form_doc_data.update({objfield: objvalue})
    return form_doc_data

def _mix_prev_draft_with_form_data(draft_object_detail, request):
    form_doc_data = {}
    existing_draft_data = draft_object_detail.get('doc_data')
    previous_draft_data = draft_object_detail.get('draft_data')
    existing_draft_data.update(previous_draft_data)
    print('full detail_draft', existing_draft_data)
    for objfield in existing_draft_data:
        objvalue = request.POST.get(objfield)
        if  objvalue:
            form_doc_data.update({objfield: objvalue})
    print('form data current: ', form_doc_data)
    previous_draft_data.update(form_doc_data)
    print('form data with previous draft: ', previous_draft_data)
    return previous_draft_data

def _update_draft_data(flexc, draft_object_detail, form_doc_data):
    wfdoc_name =  draft_object_detail.get('name')
    doctype = draft_object_detail.get("associated_doctype")
    draft_data = {"draft_data": form_doc_data}
    result = flexc.wfdoc_saveasdraft(doctype, wfdoc_name, draft_data)
    return result

@validate_token_n_session()
def create_wfdoc(request, doctype):
    result = None
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient)    
    doctype_full_dict = flexc.get_wfdoctype_fulldetail(doctype)
    docdata_fields = doctype_full_dict.get('datadocfields')    
    if request.method == 'POST':
        post_data = {}   
        for fdict in docdata_fields:
            k = fdict.get('name').lower()
            v = _lower_key_dict(request.POST).get(k)
            if v: post_data.update({k: v})
        if post_data: result = flexc.create_wfdoc(doctype, post_data)
        else: result = {"status": "aborted", "message": "Blank form can not be posted"}
    template_data = {"doctype": doctype,
                     "docdata_fields": docdata_fields,
                     "result": result}
    template_name =  "wfdoc/wfdoc_create.html"        
    web_page = validate_active_session(request, template_name, template_data)
    return web_page

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
            if Upload_result and isinstance(Upload_result, dict):
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
def list_doctypes(request):    
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient)
    doctype_list = flexc.list_wfmasterObj('Doctype')    
    template_data = {"doctype_list": doctype_list,}
    template_name =  "wfdoc/doctype_lists.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page

@validate_token_n_session()
def list_wfdoc(request, doctype):
    #doctype = ''
    docdata_fields = []
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient) 
    objfields = flexc.get_wfmobj_keys('Wfdoc')
    object_list = flexc.list_wfdoc_by_doctype(doctype)    
    print('printing object list by doctype query from client .....', object_list)
    #object_list = flexc.list_wfmasterObj_by_key_val('Wfdoc', 'associated_doctype_name', doctype)
    if object_list and isinstance(object_list, list):
        anyObj = object_list[0]
        if isinstance(anyObj.get('associated_doctype'), dict):
            doctype = anyObj.get('associated_doctype').get('name')
        else:
            doctype = anyObj.get('associated_doctype')
        docdata_fields = [k for k in anyObj.get('doc_data').keys()] #TODO: order the keys as per config
    template_data = {"objname": 'Wfdoc',
                     "doctype": doctype, #local variable 'doctype' referenced before assignment
                     "docdata_fields": docdata_fields,
                     "objfields": objfields,
                     "object_list": object_list,}
    template_name =  "wfdoc/wfdoc_list.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page

@validate_token_n_session()
def update_wfdoc(request, filter_by_name):
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient)
    object_detail = flexc.get_wfdoc_fulldetail(filter_by_name)
    data_fields, result = _get_fieldnames_from_object(object_detail)
    if request.method == 'POST':
        button_action = request.POST.get('button_action')
        form_doc_data = _get_relv_fields_fm_post_using_doc_data_struc(object_detail, request)
        input_data = {"wfdoc_name": object_detail.get('name'),
                       "intended_action": button_action}
        if form_doc_data: input_data.update({'doc_data': form_doc_data})
        if button_action.lower().strip() == "saveasdraft":
            wfdoc_name =  object_detail.get('name')
            doctype = object_detail.get("associated_doctype")
            draft_data = {"draft_data": form_doc_data}
            result = flexc.wfdoc_saveasdraft(doctype, wfdoc_name, draft_data)
        else:
            result = flexc.wfdoc_update(input_data)
    template_data = {"objname": 'Wfdoc',
                     "data_fields": data_fields,
                     #"objfields": objfields,
                     #"doctypes": doctypes,
                     #"wfstatus_list": wfstatus_list,
                     "object_detail": object_detail,                    
                     "result": result,}
    template_name =  "wfdoc/wfdoc_edit.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page

@validate_token_n_session()
def list_drafts(request, doctype):
    docdata_fields = []
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient) 
    objfields = flexc.get_wfmobj_keys('Wfdoc')
    object_list = flexc.list_drafts(doctype)
    print('draft lists...........', object_list)
    if object_list and isinstance(object_list, list):
        for Obj in object_list:
            if Obj.get('doc_data'):
                anyObj = Obj
                print('found object ', anyObj)
                break
        if isinstance(anyObj.get('associated_doctype'), dict):
            doctype = anyObj.get('associated_doctype').get('name')
        else:
            doctype = anyObj.get('associated_doctype')
        docdata_fields = [k for k in anyObj.get('doc_data').keys() ] #TODO: order the keys as per config
        filter_actions = set([','.join(obj.get('current_actions')) for obj in object_list])
    template_data = {"objname": 'Wfdoc',
                     "doctype": doctype, #local variable 'doctype' referenced before assignment
                     "docdata_fields": docdata_fields,
                     "objfields": objfields,
                     "object_list": object_list,
                     "filter_actions": filter_actions, 
                     }
    template_name =  "wfdoc/draft_list.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page

@validate_token_n_session()
def update_from_draft(request, filter_by_name):
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient)    
    draft_object_detail = flexc.detail_draft(filter_by_name, replace_orig_data=True)
    #print('draft_object_detail:   ', draft_object_detail)
    data_fields, result = _get_fieldnames_from_object(draft_object_detail)
    if request.method == 'POST':
        button_action = request.POST.get('button_action')
        form_doc_data = _mix_prev_draft_with_form_data(draft_object_detail, request)
        #print('form_doc_data along with previous draft')
        if button_action.lower().strip() == "saveasdraft":            
            result = _update_draft_data(flexc, draft_object_detail, form_doc_data)
        else:
            addl_input = {"addl_input": form_doc_data}
            result = flexc.action_from_draft(draft_object_detail.get('name'), 
                                             button_action, addl_input)
    template_data = {"objname": 'Wfdoc',
                     "data_fields": data_fields,
                     "object_detail": draft_object_detail,                    
                     "result": result,}
    template_name =  "wfdoc/detail_draft.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page

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
            if  objfield in fields_for_text_to_list_conversion :
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
#         if k in  ["permitted_to_roles", "status_needed_edit"]:
#             strv = ','.join(v)
#             object_detail.update({k: strv})
    if request.method == 'POST':
        post_data = object_detail
        for objfield in objfields:
            objvalue = request.POST.get(objfield)
            if  objvalue:
                post_data.update({objfield: objvalue})
            if objfield == "associated_doctype":
                post_data.update( {objfield: {"name": objvalue}})
            if  objfield in fields_for_text_to_list_conversion :
                objvalue = request.POST.get(objfield).split(',')
                post_data.update( {objfield: objvalue})
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





def abc():
    
    #search_filter = {"name": filter_by_name}
    #object_detail = flexc.list_wfmasterObj_by_key_val('Wfdoc', 'name', filter_by_name)
    #objfields = flexc.get_wfmobj_keys('Wfdoc')
    #doctypes = flexc.list_wfmasterObj('Doctype')
    #wfstatus_list = flexc.list_wfmasterObj('Wfstatus')   # this line is not required 
    pass
