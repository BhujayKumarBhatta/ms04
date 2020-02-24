from dashapp.tokenleader.tllogin import validate_active_session, validate_token_n_session
from dashapp.tokenleader import tllogin
from clientflexflow.client import clientflexflow


@validate_token_n_session()
def add_wfmobj(request, objname):
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient) 
    objfields = flexc.get_wfmobj_keys(objname)
    doctypes = flexc.list_wfmasterObj('Doctype')
    wfstatus = flexc.list_wfmasterObj('Wfstatus')
    result = None       
    if request.method == 'POST':
        post_data = {}
        for objfield in objfields:
            objvalue = request.POST.get(objfield)
            if  objfield == "associated_doctype":
                objvalue = {"name": request.POST.get(objfield)}
            if  objfield == "permitted_to_roles":
                objvalue = request.POST.get(objfield).split(',')
            post_data.update({objfield: objvalue})
        result = flexc.add_wfmasterObj(objname, [post_data])
    template_data = {"objname": objname,
                     "objfields": objfields,
                     "doctypes": doctypes,
                     "wfstatus": wfstatus,
                     "result": result}
    template_name =  "admin_pages/add_wfmobj.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page

