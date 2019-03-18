from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from tokenleaderclient.client.client import Client 
from micros1client.client   import MSClient
from linkinvclient.client import LIClient
from django.views.generic.edit import FormView
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
import json
 


import json


'''
How the auth_result look
{'service_catalog': 
                    {'tokenleader': 
                                   {'endpoint_url_admin': None, 
                                   'endpoint_url_external': None, 
                                   'name': 'tokenleader', 
                                   'endpoint_url_internal': 'localhost:5001', 
                                   'id': 1}, 
                    'linkInventory': {'endpoint_url_admin': None, 
                    'endpoint_url_external': 'https://192.168.111.141:5004', 
                    'name': 'linkInventory', 
                    'endpoint_url_internal': 'https://192.168.111.141:5004', 
                    'id': 2}}, 
'status': 'success', 
'message': 'success', 
'auth_token': 'AA'}

'''


#class SubscribeView(FormView):
#    template_name = 'subscribe-form.html'
#    form_class = SubscribeForm
#    success_url = reverse_lazy('form_data_valid')
def prep_tlclient_from_session(request):
    if 'uname' in request.session and 'psword' in request.session:
        uname = request.session['uname']
        psword = request.session['psword']
        auth_config = Configs(tlusr=uname, tlpwd=psword)
        tlclient = Client(auth_config) 
        return   tlclient 
            

# Create your views here.
def login(request):    
    if request.method == 'GET':   
        txt = "Enter user name and password to get access to  dashboard"
        template_data = {"mykey": txt }     
        result = render(request, 'login.html', template_data)        
    elif request.method == 'POST':
        uname = request.POST.get('username', '')
        psword = request.POST.get('password', '')
        request.session['uname'] = uname
        request.session['psword'] = psword
        auth_config = Configs(tlusr=uname, tlpwd=psword)
        tlclient = Client(auth_config)        
        auth_result = tlclient.get_token()        
        auth_result_json = json.dumps(auth_result)
        if auth_result.get('status') != 'success':
            txt = auth_result.get('message')  
            template_data = {"mykey": txt }          
            result = render(request, 'login.html', template_data)            
        else:       
            #result = HttpResponse(auth_result_json)
            verified_token = tlclient.verify_token(auth_result.get('auth_token'))
            if verified_token.get('status') == 'Invalid token':
                txt = verified_token.get('message')  
                template_data = {"mykey": txt }          
                result = render(request, 'login.html', template_data) 
                
            else:
                template_data = {"service_catalog": auth_result.get('service_catalog'),
                                "user_details": verified_token.get('payload').get('sub'),
                                }           
                
                result = render(request, 'home.html', template_data)
            
    return result


def list_users(request):
    if request.method == 'GET': 
        tlclient = prep_tlclient_from_session(request)
        list_users = tlclient.list_users()
        template_data = {"list_users": list_users.get('status') } 
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_users))
        return result


def adduser(request):
    if request.method == 'GET': 
        #tlclient = prep_tlclient_from_session(request)
        #list_users = tlclient.list_users()
        template_data = {"ADDUSER": "TRUE" }  
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_users))
        return result

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

    
    
def list_links(request):
    if request.method == 'GET': 
        tlclient = prep_tlclient_from_session(request)
        lic = LIClient(tlclient)
        list_links = lic.list_links()
        template_data = {"list_links": list_links.get('message') } 
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_links))
        return result


def list_test(request):
    if request.method == 'GET': 
        _param1 = request.GET['from']
        _param2 = request.GET['name']
        response = 'You are name is :' + _param1 + ' and from :' + _param2
        return HttpResponse(response)   

    
### Manage Invoice Upload #####################
## List All Invoice
def list_invoices(request):
    if request.method == 'GET': 
        tlclient = prep_tlclient_from_session(request)
        invClient = MSClient(tlclient) 
        list_invoices = invClient.list_invoices('all','all')
        list_invoices = json.load(list_invoices)
        #list_invoices = invClient.list()
        template_data = {"list_invoices": list_invoices.get('message') } 
        result = render(request, 'home.html', template_data)        
        return result
## Upload Invoice******
#def list_invoices(request):
#    if request.method == 'GET': 
#        tlclient = prep_tlclient_from_session(request)
#        invClient = MSClient(tlclient) 
#        invClient.upload_xl('file Loaction')        
#        template_data = {"list_invoices": list_invoices.get('status') } 
#        result = render(request, 'home.html', template_data)        
#        return result

### End Invoice #####################