from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from  tokenleaderclient.client.client import Client 
from micros1client.client   import MSClient
import json


tlclient = None
# c = MSClient(tlclient)

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


# Create your views here.
def login(request):    
    if request.method == 'GET':   
        txt = "Enter user name and password to get access to  dashboard"
        template_data = {"mykey": txt }     
        result = render(request, 'login.html', template_data)        
    elif request.method == 'POST':
        uname = request.POST.get('username', '')
        psword = request.POST.get('password', '')
        auth_config = Configs(tlusr=uname, tlpwd=psword )
        tlclient = Client(auth_config)
        auth_result = tlclient.get_token()        
        auth_result_json = json.dumps(auth_result)
        if auth_result.get('status') != 'success':
            txt = auth_result.get('message')  
            template_data = {"mykey": txt }          
            result = render(request, 'login.html', template_data)            
        else:       
            #result =  HttpResponse(auth_result_json)
            verified_token = tlclient.verify_token(auth_result.get('auth_token'))
            if verified_token.get('status') == 'Invalid token':
                txt = verified_token.get('message')  
                template_data = {"mykey": txt }          
                result = render(request, 'login.html', template_data) 
                
            else:
                template_data = {"service_catalog": auth_result.get('service_catalog' ),
                                "user_details": verified_token.get('payload').get('sub'),
                                "user_name": uname }           
                
                result = render(request, 'home.html', template_data)
            
    return result


    
