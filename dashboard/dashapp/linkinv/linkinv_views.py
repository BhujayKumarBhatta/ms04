from dashapp.tokenleader import tllogin
from linkinvclient.client import LIClient
from micros1client.client import MSClient
from django.shortcuts import render
from dashapp.tokenleader.tllogin import validate_active_session


    
def list_links(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        lic = LIClient(tlclient)
        list_links = lic.list_links()
        #template_data = {"list_links": list_links.get('message') }
        template_data = {"list_links": list_links }
        template_name = "wanlinks/list_links.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page


def list_ravl_obj(request, objname, rolename):
    tlclient = tllogin.prep_tlclient_from_session(request)
    lic = LIClient(tlclient)
    list_ravl_obj = lic.list_obj(objname,"all","all")
    list_infoops_links = lic.list_links()
    template_data = {"list_ravl_obj": list_ravl_obj, 
                     "list_infoops_links": list_infoops_links }
    if objname == "Lnetlink":
        if rolename == "ITC" or rolename == "role1":
            template_name = "wanlinks/list_ravl_link.html"
        elif rolename == "TSP":
            template_name = "wanlinks/tsp_list_ravl_link.html" 
    if objname == "Altaddress":
        template_name = "financials/list_ravl_addr.html"
    if objname == "Rate":
        template_name = "financials/list_ravl_rate.html"
    if objname == "Payment":
        template_name = "financials/list_ravl_payment.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page


def delete_ravl(request, objname, objid):
    if request.method == "GET":
        tlclient = tllogin.prep_tlclient_from_session(request)
        lic = LIClient(tlclient)
        if objid:
            status = lic.delete_obj(objname, objid)
            template_data = {"status": status }
        else:
            template_data = {"status": "No id supplied for deletion" }
    list_ravl_link = lic.list_obj("Lnetlink","all","all")
    template_data = {"list_ravl_link": list_ravl_link }
    template_name = "wanlinks/list_ravl_link.html"    
    web_page = validate_active_session(request, template_name, template_data)
    return web_page 


def managelocalnet(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    lic = LIClient(tlclient)
    status = None
    if request.method == 'GET': 
        list_rate = lic.list_obj("Rate","all","all")        
        list_Altaddress = lic.list_obj("Altaddress","all","all")        
        list_infobahn_links = lic.list_links()
        template_data = {"list_rate":list_rate,
                         "list_Altaddress":list_Altaddress,
                         "list_infobahn_links": list_infobahn_links}
        template_name = "wanlinks/add_ravl_link.html"
    if request.method == 'POST':
        must_have = ["infoopsid", "altaddress_id", "rate_id", "last_payment_date"]
        for m in must_have:
            if m not in request.POST:
                template_data = {"status": "form has not been filled up with all necessary data" }
        lnet_d = {"infoopsid": "", "altaddress_id": 0, "rate_id": 0, "last_payment_date": ""}
        lnet_d['infoopsid'] = request.POST.get('infoopsid')
        lnet_d['altaddress_id'] = request.POST.get('altaddress_id')
        lnet_d['rate_id'] = request.POST.get('rate_id')
        lnet_d['last_payment_date'] = request.POST.get('last_payment_date')
        status = lic.add_lnetlink(lnet_d) 
        template_data = {"status": status }
        template_name = "wanlinks/exec_status.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page


def add_address(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    lic = LIClient(tlclient)
    status = None
    if request.method == 'GET': 
        template_name = "financials/add_ravl_addr.html"
        template_data = {}
    if request.method == 'POST':
        must_have = ["prem_name", "prem_no", "state", "city",
                     "pin", "gstn", "sgst_rate", "cgst_rate"]
        for m in must_have:
            if m not in request.POST:
                template_data = {"status": "form has not been filled up with all necessary data" }
        all_add = {"prem_name": "", "prem_no": 0, "state": "", 
                   "city": "", "pin": 0, "gstn": "", "sgst_rate": 0, 
                   "cgst_rate": 0}
        all_add['prem_name'] = request.POST['prem_name']
        all_add['prem_no'] = request.POST['prem_no']
        all_add['state'] = request.POST['state']
        all_add['city'] = request.POST['city']
        all_add['pin'] = request.POST['pin']        
        all_add['gstn'] = request.POST['gstn']        
        all_add['sgst_rate'] = request.POST['sgst_rate']        
        all_add['cgst_rate'] = request.POST['cgst_rate'] 
        status = lic.add_altaddress(all_add)
        template_data = {"status": status }
        template_name = "wanlinks/exec_status.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page


def add_rate(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    lic = LIClient(tlclient)
    status = None
    if request.method == 'GET': 
        template_name = "financials/add_ravl_rate.html"
        template_data = {}
    if request.method == 'POST':
        must_have = ["tsp", "linktype", "otc", "activity_type",
                     "rate_per_year",]
        for m in must_have:
            if m not in request.POST:
                template_data = {"status": "form has not been filled up with all necessary data" }
        rate_dict = {'tsp': '', 'linktype': '', 'activity_type': '', 'otc': 0, 'rate_per_year': 0 }
        rate_dict['tsp'] = request.POST['tsp']
        rate_dict['linktype'] = request.POST['linktype']
        rate_dict['otc'] = request.POST['otc']
        rate_dict['activity_type'] = request.POST['activity_type']
        rate_dict['rate_per_year'] = request.POST['rate_per_year']
        status = lic.add_rate(rate_dict)
        template_data = {"status": status }
        template_name = "wanlinks/exec_status.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page


def add_payment(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    lic = LIClient(tlclient)
    status = None
    if request.method == 'GET':
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_Lnetlink = lic.list_obj("Lnetlink","all","all")
        template_name = "financials/add_ravl_payment.html"
        template_data = {"list_Lnetlink": list_Lnetlink}
    if request.method == 'POST':
        must_have = ["invoice_id", "billing_from", "billing_to", "billing_type",
                     "amount", "payment_date", "mode", "ref_no", "status", "netlink_id"]
        for m in must_have:
            if m not in request.POST:
                template_data = {"status": "form has not been filled up with all necessary data" }
        payment_dict = {"invoice_id": "", "billing_from": "01-01-2019", 
                        "billing_to": "31-03-2019", "billing_type": "Installation",
                        "amount": "0", "payment_date": "", "mode": "", "ref_no": "", 
                        "status": "", "netlink_id": 0}
        payment_dict['invoice_id'] = request.POST['invoice_id']
        payment_dict['billing_from'] = request.POST['billing_from']
        payment_dict['billing_to'] = request.POST['billing_to']
        payment_dict['billing_type'] = request.POST['billing_type']
        payment_dict['amount'] = request.POST['amount']        
        payment_dict['payment_date'] = request.POST['payment_date'] 
        payment_dict['mode'] = request.POST['mode']         
        payment_dict['ref_no'] = request.POST['ref_no']        
        payment_dict['status'] = request.POST['status']        
        payment_dict['netlink_id'] = request.POST['netlink_id']       
        status = lic.add_payment(payment_dict)   
        template_data = {"status": status }
        template_name = "wanlinks/exec_status.html"
    web_page = validate_active_session(request, template_name, template_data)
    return web_page

