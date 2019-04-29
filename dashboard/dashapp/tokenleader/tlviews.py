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
        #list_users = tlclient.list_users()
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
        print(email)
        roles = request.POST.get('roles')
        print(roles)
        wfc = request.POST.get('wfc')
        newuserdata = dict({"username": "", "email": "", "password": "", "wfc": "", "roles": ""})	
        print(newuserdata)
        newuserdata["username"]= username
        newuserdata["email"]= email
        newuserdata["wfc"]= wfc
        newuserdata["password"]= password
        newuserdata["role"] = roles
        tlclient = tllogin.prep_tlclient_from_session(request)
        status = tlclient.add_user(newuserdata)
        list_users = tlclient.list_users()
        template_data = {"list_users": list_users.get('status') } 
        result = render(request, 'home.html', template_data)
        return result
				
def delete_user(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        username = request.POST['username']
        data = dict({"username": ""})
        #data = {"username": "user2"}
        data["username"] = username 
        status = tlclient.delete_user(data)
        list_org = tlclient.delete_user()
        template_data = {"delete_user": delete_user }
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
        status = tlclient.add_dept(data)
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
        status = tlclient.delete_dept(data)
        list_dept = tlclient.list_dept()
        template_data = {"list_dept": list_dept }
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
        status = tlclient.add_role(data)
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
        status = tlclient.delete_role(data)
        list_role = tlclient.list_role()
        template_data = {"list_role": list_role }
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
        status = tlclient.add_orgunit(data)
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
        status = tlclient.delete_ou(data)
        list_ou = tlclient.list_ou()
        template_data = {"list_ou": list_ou }
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
        data = dict({"orgname": ""})
        #data = {"oname": "org2"}
        data["oname"] = orgname 
        status = tlclient.add_org(data)
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
        status = tlclient.delete_org(data)
        list_org = tlclient.list_org()
        template_data = {"list_org": list_org }
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
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        wfcname = request.POST['wfcname']
        data = dict({"ouname": ""})
        #data = {"ouname": "ou2"}
        data["ouname"] = ouname 
        status = tlclient.add_orgunit(data)
        list_ou = tlclient.list_ou()
        template_data = {"list_ou": list_ou }
        result = render(request, 'home.html', template_data)
        return result
        		
def delete_wfc(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        wfcname = request.POST['wfcname']
        data = dict({"wfcname": ""})
        data["wfcname"] = wfcname 
        status = tlclient.delete_wfc(data)
        list_wfc = tlclient.list_wfc()
        template_data = {"delete_wfc": delete_wfc}
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
        		

