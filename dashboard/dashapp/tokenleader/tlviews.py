import json
from dashapp.tokenleader import tllogin
from linkinvclient.client import LIClient
from django.shortcuts import render
from dashapp.tokenleader.tllogin import validate_active_session, validate_token_n_session


def list_users(request):
    token_expiry, template_data, template_name = False, {}, {}
    if request.method == 'GET':        
        tlclient = tllogin.prep_tlclient_from_session(request)
        if tlclient:
            list_users = tlclient.list_users()
            template_data = {"list_users": list_users.get('status')}
            template_name = 'admin_pages/list_users.html'
        else:
            token_expiry=True
        web_page = validate_active_session(request, template_name,
                                           template_data, token_expiry)
        return web_page


def adduser(request):
    if request.method == 'GET':
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_users = tlclient.list_users()
        org_list = tlclient.list_org()
        role_list = tlclient.list_role()
        wfc_list = tlclient.list_wfc()				
        template_data = {"ORGLIST":org_list,
                         "ROLELIST":role_list,"WFCLIST":wfc_list}
        template_name =  'admin_pages/add_user.html'
        web_page = validate_active_session(request, template_name,
                                           template_data)
        return web_page 
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')		
        email = request.POST.get('email')
        roles = request.POST.get('role')
        wfc = request.POST.get('wfc')
        otpmode = request.POST.get('otpmode')
        allowemaillogin = request.POST.get('allowemaillogin')
        tlclient = tllogin.prep_tlclient_from_session(request)
        status = tlclient.add_user(username,password,email,roles,wfc, otpmode)
        list_users = tlclient.list_users()
        template_data = {"list_users": list_users.get('status'),
                         "STATUS_ADDUSER": status }
        template_name = 'admin_pages/status_modal.html'  
        web_page = validate_active_session(request, template_name,
                                           template_data)
        return web_page


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
        template_name = 'admin_pages/list_users.html'
        web_page = validate_active_session(request, template_name, 
                                           template_data)
        return web_page
     
@validate_token_n_session()      
def list_org(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_org = tlclient.list_org()
        template_data = {"list_org": list_org } 
        template_name = 'admin_pages/list_org.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page    
  
          
def add_org(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_org = tlclient.list_org()
        org_list = tlclient.list_org() 
        template_data = {"ORGLIST":org_list}
        template_name =  'admin_pages/add_org.html'
        web_page = validate_active_session(request, template_name, template_data)
        return web_page 

    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        orgname = request.POST['orgname']
        data = dict({"orgname": ""})
        #data = {"oname": "org2"}
        #data["username"] = username
        #data["oname"] = orgname         
        #status = tlclient.add_org(data)
        status = tlclient.add_org(orgname)
        list_org = tlclient.list_org()
        template_data = {"list_org": list_org}
        template_name = 'admin_pages/list_org.html'
        web_page = validate_active_session(request, template_name, template_data)
        return web_page 

           
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
        template_data = {"list_org": list_org}
        template_name = 'admin_pages/list_org.html'
        web_page = validate_active_session(request, template_name, template_data)
        return web_page


def list_dept(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_dept = tlclient.list_dept()
        template_data = {"list_dept": list_dept } 
        template_name = 'admin_pages/list_dept.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page 
        		
def add_dept(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_dept = tlclient.list_dept()
        dept_list = tlclient.list_dept() 
        template_data = {"list_dept": list_dept }
        template_name =  'admin_pages/add_dept.html'
        web_page = validate_active_session(request, template_name, template_data)
        return web_page 
        
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
        template_name = 'admin_pages/list_dept.html'
        web_page = validate_active_session(request, template_name, template_data)
        return web_page

def delete_dept(request):
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        deptname = request.POST['deptname']
        data = dict({"deptname": ""})
        data["deptname"] = deptname 
        status = tlclient.delete_dept(deptname)
        list_dept = tlclient.list_dept()
        template_data = {"list_dept": list_dept}
        template_name = 'admin_pages/list_dept.html'
        web_page = validate_active_session(request, template_name, template_data)
        return web_page
 
def list_role(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_role = tlclient.list_role()
        template_data = {"list_role": list_role } 
        template_name = 'admin_pages/list_role.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page        
      		
def add_role(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_role = tlclient.list_role()
        role_list = tlclient.list_role() 
        template_data = {"list_dept": list_role }
        template_name =  'admin_pages/add_role.html'
        web_page = validate_active_session(request, template_name, template_data)
        return web_page
        
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
        template_name = 'admin_pages/list_role.html'
        web_page = validate_active_session(request, template_name, template_data)
        return web_page  
        		
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
        template_data = {"list_role": list_role}
        template_name = 'admin_pages/list_role.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page 

def list_ou(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_ou = tlclient.list_ou()
        template_data = {"list_ou": list_ou } 
        template_name = 'admin_pages/list_ou.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page  

def add_ou(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_ou = tlclient.list_ou()
        template_data = {"list_ou": list_ou } 
        template_name = 'admin_pages/add_ou.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page  
        
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
        template_name = 'admin_pages/list_ou.html'
        web_page = validate_active_session(request, template_name, template_data)
        return web_page  

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
        template_data = {"list_ou": list_ou}
        template_name = 'admin_pages/list_ou.html'
        web_page = validate_active_session(request, template_name, template_data)
        return web_page  	 		

def list_wfc(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_wfc = tlclient.list_wfc()
        template_data = {"list_wfc": list_wfc } 
        template_name = 'admin_pages/list_wfc.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page  
        		
def add_wfc(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_wfc = tlclient.list_wfc()
        list_org = tlclient.list_org()
        list_ou = tlclient.list_ou()
        list_dept = tlclient.list_dept()				
        template_data = {"ADDWFC": "TRUE","ORGLIST":list_org,"OULIST":list_ou,"DEPTLIST":list_dept}  
        template_name = 'admin_pages/add_wfc.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page  
         
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
        template_name = 'admin_pages/list_wfc.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page  
        		
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
        template_name = 'admin_pages/list_wfc.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page  


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
        template_name = 'admin_pages/list_service.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page  
    
def add_service(request):
    if request.method == 'GET':  
        tlclient = tllogin.prep_tlclient_from_session(request)
        list_services = tlclient.list_service()
        template_data = {"list_services": list_services }        
        template_name = 'admin_pages/add_service.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page  
        
    if request.method == 'POST':
        tlclient = tllogin.prep_tlclient_from_session(request)
        servicename = request.POST['servicename']
        urlinternal = request.POST['urlinternal']
        urlexternal = request.POST['urlexternal']
        urladmin = request.POST['urladmin']                
        status = tlclient.add_service(servicename,urlinternal, urlexternal ,urladmin)
        list_services = tlclient.list_service()
        template_data = {"list_services": list_services}
        template_name = 'admin_pages/list_service.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page    

def delete_service(request):
    if request.method == 'POST': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        servicename = request.POST['servicename']
        status = tlclient.delete_service(servicename)
        list_services = tlclient.list_service()
        template_data = {"list_services": list_services }
        template_name = 'admin_pages/list_service.html'
        web_page = validate_active_session(request, template_name, template_data)       
        return web_page  
        
