import json
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from tokenleaderclient.client.client import Client

from django.conf import settings
#from django.contrib import auth
#from datetime import datetime, timedelta
#from .settings import EXPIRE_AFTER, PASSIVE_URLS, PASSIVE_URL_NAMES


#class SubscribeView(FormView):
#    template_name = 'subscribe-form.html'
#    form_class = SubscribeForm
#    success_url = reverse_lazy('form_data_valid')


def prep_tlclient_from_session(request):
    if 'uname' in request.session and 'psword' in request.session:
        uname = request.session = ""
        psword = request.session - ""	
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



################ SESSION MANAGEMENT ######################
#def get_expire_seconds(self, request):
#    """Return time (in seconds) before the user should be logged out."""
#    return EXPIRE_AFTER

#def process_request(self, request):
#    if not request.user.is_authenticated() :
#        #Can't log out if not logged in
#        return
#    try:
#        if datetime.now() - request.session['last_touch'] > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
#            logout(request)
#            del request.session['last_touch']
#            return
#    except KeyError:
#        pass
#    request.session['last_touch'] = datetime.now()

#def logout(request):    
#    template_data = {"SESSION_EXPIRED": "Your Session got Expired Please login!"}          
#    result = render(request, 'login.html', template_data)                 
#    return result

############### END ######################
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
    
