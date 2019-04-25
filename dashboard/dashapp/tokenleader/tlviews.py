import json
from dashapp.tokenleader import tllogin
from linkinvclient.client import LIClient
from django.shortcuts import render

## Token Leader Module ****************************************************
def list_users(request):
    if request.method == 'GET':  
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_users = tlclient.list_users()
        template_data = {"list_users": list_users.get('status') } 
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_users))
        return result

def list_org(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_org = tlclient.list_org()
        list_org = json.dumps(list_org)
        list_org = json.loads(list_org)
        template_data = {"list_org": list_org } 
        result = render(request, 'home.html', template_data)         
        return result

def list_dept(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_dept = tlclient.list_dept()
        #list_dept = json.dumps(list_dept)
        #list_dept = json.loads(list_dept)
        template_data = {"list_dept": list_dept } 
        result = render(request, 'home.html', template_data)         
        return result

def list_role(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_role = tlclient.list_role()
        #list_role = json.dumps(list_role)
        template_data = {"list_role": list_role } 
        result = render(request, 'home.html', template_data)         
        return result

def list_ou(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_ou = tlclient.list_ou()
        #list_ou = json.dumps(list_ou)
        template_data = {"list_ou": list_ou } 
        result = render(request, 'home.html', template_data)         
        return result


def adduser(request):
    if request.method == 'GET': 
        #tlclient = prep_tlclient_from_session(request)
        #list_users = tlclient.list_users()
        template_data = {"ADDUSER": "TRUE" }  
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_users))
        return result

## End ****************************************************
def invoice(request):
    if request.method == 'GET': 
        #tlclient = prep_tlclient_from_session(request)
        #list_users = tlclient.list_users()
        template_data = {"INVOICE": "TRUE" }  
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_users))
        return result

def po(request):
    if request.method == 'GET': 
        #tlclient = prep_tlclient_from_session(request)
        #list_users = tlclient.list_users()
        template_data = {"PO": "TRUE" }  
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_users))
        return result

def invoice_upload(request):
    if request.method == 'GET': 
        #tlclient = prep_tlclient_from_session(request)
        #list_users = tlclient.list_users()
        template_data = {"INVICE_UPLOAD": "TRUE" }  
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_users))
        return result
        		
        		
				
def org_delete(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        orgname = request.POST['orgname']		 
        data = dict({ "oname": ""})
   	data = {"oname": "orgname"}
        status = tlclient.delete_org(data) 
        list_org = tlclient.list_org()     
        template_data = {"list_org": list_org } 
        result = render(request, 'home.html', template_data)
        return result  
#//	except Exception as exception:
#//		 	tlclient = tllogin.prep_tlclient_from_session(request)
#//		 	list_org = tlclient.list_org()
#//	        list_org = json.dumps(list_org)
#//	        list_org = json.loads(list_org)
#//	        template_data = {"list_org": list_org,"Exception": exception,"EXCEPTION_INFO" : sys.exc_info()[0] }	 
#//			result = render(request, 'home.html', template_data)
#//	        return result  
       

