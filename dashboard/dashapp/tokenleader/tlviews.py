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
        		
#=========adduser pending        		
def adduser(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_users = tlclient.list_users()
        org_list = tlclient.list_org()
        role_list = tlclient.list_role()
        wfc_list = tlclient.list_wfc()				
        template_data = {"ADDUSER": "TRUE","ORGLIST":org_list,"ROLELIST":role_list,"WFCLIST":wfc_list}  
        result = render(request, 'home.html', template_data)        
        return result   
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')		
        email = request.POST.get('email')
        roles = request.POST.get('role')
        wfc = request.POST.get('wfc')
        newuserdata = dict({"username": "", "email": "", "password": "", "wfc": "", "roles": [""]})
        newuserdata["username"]= username
        newuserdata["email"]= email
        newuserdata["wfc"]= wfc
        newuserdata["password"]= password
        newuserdata["roles"][0] = roles
        tlclient = tllogin.prep_tlclient_from_session(request)
        #status = tlclient.add_user(newuserdata)
        status = tlclient.add_user(username,password,email,roles,wfc,'mail')
        list_users = tlclient.list_users()
        #template_data = {"list_users": list_users,"STATUS_ADDUSER": status} 
        template_data = {"list_users": list_users.get('status'),"STATUS_ADDUSER": status }
        result = render(request, 'home.html', template_data)
        return result
				
def delete_user(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        username = request.POST['username']
        data = dict({"username": ""})
        #data = {"username": "user2"}
        data["username"] = username 
        #status = tlclient.delete_user(data)
        status = tlclient.delete_user(username)
        list_users = tlclient.list_users()
        template_data = {"list_users": list_users.get('status'), "DELETE_STATUS": status}
        result = render(request, 'home.html', template_data)
        return result

def list_dept(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_dept = tlclient.list_dept()
        list_dept = json.dumps(list_dept)
        list_dept = json.loads(list_dept)
        template_data = {"list_dept": list_dept } 
        result = render(request, 'home.html', template_data)         
        return result
        		
def add_dept(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        deptname = request.POST['deptname']
        data = dict({"deptname": ""})
        #data = {"deptname": "dept2"}
        data["deptname"] = deptname 
        #status = tlclient.add_dept(data)
        status = tlclient.add_dept(deptname)
        list_dept = tlclient.list_dept()
        template_data = {"list_dept": list_dept }
        result = render(request, 'home.html', template_data)
        return result
        		
def delete_dept(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        deptname = request.POST['deptname']
        data = dict({"deptname": ""})
        #data = {"deptname": "dept2"}
        data["deptname"] = deptname 
        #status = tlclient.delete_dept(data)
        status = tlclient.delete_dept(deptname)
        list_dept = tlclient.list_dept()
        template_data = {"list_dept": list_dept ,"DELETE_STATUS":status}
        result = render(request, 'home.html', template_data)
        return result

def list_role(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_role = tlclient.list_role()
        list_role = json.dumps(list_role)
        list_role = json.loads(list_role)
        template_data = {"list_role": list_role } 
        result = render(request, 'home.html', template_data)         
        return result
        		
def add_role(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        rolename = request.POST['rolename']
        data = dict({"rolename": ""})
        #data = {"rolename": "role2"}
        data["rolename"] = rolename 
        #status = tlclient.add_role(data)
        status = tlclient.add_role(rolename)
        list_role = tlclient.list_role()
        template_data = {"list_role": list_role }
        result = render(request, 'home.html', template_data)
        return result
        		
def delete_role(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        rolename = request.POST['rolename']
        data = dict({"rolename": ""})
        #data = {"rolename": "role2"}
        data["rolename"] = rolename 
        #status = tlclient.delete_role(data)
        status = tlclient.delete_role(rolename)
        list_role = tlclient.list_role()
        template_data = {"list_role": list_role ,"DELETE_STATUS":status}
        result = render(request, 'home.html', template_data)
        return result

def list_ou(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_ou = tlclient.list_ou()
        list_ou = json.dumps(list_ou)
        list_ou = json.loads(list_ou)
        template_data = {"list_ou": list_ou } 
        result = render(request, 'home.html', template_data)         
        return result

def add_ou(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        ouname = request.POST['ouname']
        data = dict({"ouname": ""})
        #data = {"ouname": "ou2"}
        data["ouname"] = ouname 
        #status = tlclient.add_orgunit(data)
        status = tlclient.add_orgunit(ouname)
        list_ou = tlclient.list_ou()
        template_data = {"list_ou": list_ou }
        result = render(request, 'home.html', template_data)
        return result

def delete_ou(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        ouname = request.POST['ouname']
        data = dict({"ouname": ""})
        #data = {"ouname": "ou2"}
        data["ouname"] = ouname 
        #status = tlclient.delete_ou(data)
        status = tlclient.delete_ou(ouname)
        list_ou = tlclient.list_ou()
        template_data = {"list_ou": list_ou ,"DELETE_STATUS":status}
        result = render(request, 'home.html', template_data)
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
        		
def add_org(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        orgname = request.POST['orgname']
        data = dict({"username": "","orgname": ""})
        #data = {"oname": "org2"}
        #data["username"] = username
        #data["oname"] = orgname         
        #status = tlclient.add_org(data)
        status = tlclient.add_org(orgname)
        list_org = tlclient.list_org()
        template_data = {"list_org": list_org }
        result = render(request, 'home.html', template_data)
        return result
        		
def delete_org(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        orgname = request.POST['orgname']
        data = dict({"orgname": ""})
        #data = {"oname": "org2"}
        data["oname"] = orgname 
        #status = tlclient.delete_org(data)
        status = tlclient.delete_org(orgname)
        list_org = tlclient.list_org()
        template_data = {"list_org": list_org ,"DELETE_STATUS":status}
        result = render(request, 'home.html', template_data)
        return result
	
def list_wfc(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_wfc = tlclient.list_wfc()
        list_wfc = json.dumps(list_wfc)
        list_wfc = json.loads(list_wfc)
        template_data = {"list_wfc": list_wfc } 
        result = render(request, 'home.html', template_data)         
        return result      
        		
def add_wfc(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_wfc = tlclient.list_wfc()
        list_org = tlclient.list_org()
        list_ou = tlclient.list_ou()
        list_dept = tlclient.list_dept()				
        template_data = {"ADDWFC": "TRUE","ORGLIST":list_org,"OULIST":list_ou,"DEPTLIST":list_dept}  
        result = render(request, 'home.html', template_data)        
        return result   
    if request.method == 'POST':    
        fname = request.POST.get('fname')
        orgname = request.POST.get('orgname')		
        ou_name = request.POST.get('ou_name')
        dept_name = request.POST.get('dept_name')
        newfcdata = dict({"fname": "", "orgname": "", "ou_name": "", "dept_name": ""})
        newfcdata["fname"]= fname
        newfcdata["orgname"]= orgname
        newfcdata["ou_name"]= ou_name
        newfcdata["dept_name"]= dept_name
        tlclient = tllogin.prep_tlclient_from_session(request)
        #status = tlclient.add_wfc(newfcdata)
        status = tlclient.add_wfc(fname, orgname, ou_name, dept_name)
        list_wfc = tlclient.list_wfc()
        template_data = {"list_wfc": list_wfc } 
        result = render(request, 'home.html', template_data)
        return result
        		
def delete_wfc(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        wfcname = request.POST['wfcname']
        data = dict({"wfcname": ""})
        data["wfcname"] = wfcname 
        #status = tlclient.delete_wfc(data)
        status = tlclient.delete_wfc(wfcname)
        list_wfc = tlclient.list_wfc()
        template_data = {"delete_wfc": delete_wfc,"list_wfc": list_wfc,"DELETE_STATUS":status}
        result = render(request, 'home.html', template_data)
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
        		

def list_service(request):
    if request.method == 'GET':  
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_services = tlclient.list_service()
        template_data = {"list_services": list_services }
        result = render(request, 'home.html', template_data)
        return result
    
def add_service(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        servicename = request.POST['servicename']
        urlinternal = request.POST['urlinternal']
        urlexternal = request.POST['urlexternal']
        urladmin = request.POST['urladmin']                
        status = tlclient.add_service(servicename,urlinternal, urlexternal ,urladmin)
        list_services = tlclient.list_service()
        template_data = {"list_services": list_services ,'addstatus' : status}
        result = render(request, 'home.html', template_data)
        return result

def delete_service(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        servicename = request.POST['servicename']
        status = tlclient.delete_service(servicename)
        list_services = tlclient.list_service()
        template_data = {"list_services": list_services ,'DELETE_STATUS' : status}
        result = render(request, 'home.html', template_data)       
        return result
