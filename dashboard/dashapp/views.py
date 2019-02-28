from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from  tokenleaderclient.client.client import Client 
from micros1client.client   import MSClient
import json


tlclient = None
# c = MSClient(tlclient)


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
            result =  HttpResponse(auth_result_json)
            
    return result


    
