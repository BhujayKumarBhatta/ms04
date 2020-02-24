from dashapp.tokenleader.tllogin import validate_active_session, validate_token_n_session
from dashapp.tokenleader import tllogin
from clientflexflow.client import clientflexflow


@validate_token_n_session()
def add_wfmobj(request, objname):
    tlclient = tllogin.prep_tlclient_from_session(request)
    flexc = clientflexflow(tlclient) 
    objfields = flexc.get_wfmobj_keys(objname)
    result = None       
    if request.method == 'POST':
        post_data = {}
        for objfield in objfields:            
            post_data.update({objfield: request.POST.get(objfield)})
        result = flexc.add_wfmasterObj(objname, post_data)
    template_data = {"objname": objname,
                     "objfields": objfields,
                     "result": result}
    template_name =  "admin_pages/add_wfmobj.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page