import json
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from tokenleaderclient.client.client import Client

from django.conf import settings
#from django.contrib import auth
from datetime import datetime, timedelta
#from .settings import EXPIRE_AFTER, PASSIVE_URLS, PASSIVE_URL_NAMES


def prep_tlclient_from_session(request):
    if 'uname' and 'domain' in request.session:
        uname = request.session.get('uname')
        domain = request.session.get('domain')
        psword = request.session.get('psword')
        otp = request.session.get('otp')
        #print('got domain, pasword, otp from session as:', domain, psword, otp)
        if psword:
            print("initializing tlclient with passowrd")
            auth_config = Configs(tlusr=uname, tlpwd=psword, domain=domain)
        elif otp:
            print("initializing tlclient with OTP")
            auth_config = Configs(tlusr=uname, otp=otp, domain=domain)
        tlclient = Client(auth_config)
        return   tlclient 
            

#This is serves both home and login page
def login(request):    
    if request.method == 'GET':
        #check if the session already has credentials
        web_page = validate_active_session(request,'home.html', {} )
        return web_page 
    elif request.method == 'POST':
        uname = request.POST.get('username', '')
        psword = request.POST.get('password', '')
        domain = request.POST.get('domain', '')        
        request.session['uname'] = uname
        request.session['psword'] = psword
        request.session['domain'] = domain
        print("pushed domain in session as:", domain, request.session['domain'])        
        request.session['last_clicked_on'] = datetime.now().timestamp()
        if request.POST.get('otp', ''):
            otp = request.POST.get('otp', '')
            request.session['otp'] = otp
            auth_config = Configs(tlusr=uname, otp=otp, domain=domain)
        else:
            auth_config = Configs(tlusr=uname, tlpwd=psword, domain=domain)
        tlclient = Client(auth_config)        
        auth_result = tlclient.get_token()        
        auth_result_json = json.dumps(auth_result)
        print(auth_result_json)
        if auth_result.get('status') != 'success' and auth_result.get('status') !='OTP_SENT' :
            txt = auth_result.get('message')  
            template_data = {"mykey": txt }          
            result = render(request, 'login.html', template_data)
        elif auth_result.get('status') == 'OTP_SENT':           
            txt = auth_result.get('message')
            print(txt)
            template_data = {"mykey": txt, 
                             "otp_login": True,
                             "domain": domain,
                             "uname": uname}          
            result = render(request, 'login_otp.html', template_data)           
        else:       
            #result = HttpResponse(auth_result_json)
            verified_token = tlclient.verify_token(auth_result.get('auth_token'))
            if verified_token.get('status') == 'Invalid token':
                txt = verified_token.get('message')  
                template_data = {"mykey": txt }          
                result = render(request, 'login.html', template_data) 
                
            else:
                user_details = verified_token.get('payload').get('sub')
                template_data = {"service_catalog": auth_result.get('service_catalog'),
                                "user_details": user_details,
                                "login_time": datetime.now()
                                }           
                request.session['session_user_details'] = user_details
                result = render(request, 'home.html', template_data)
            
    return result

def logout(request):
    request.session['session_user_details'] = None
    request.session['uname'] = None
    request.session['psword'] = None
    request.session['domain'] = None
    request.session['otp'] = None
    request.session['last_clicked_on'] = None
    txt = "Logged out, session expired  please login again"
    template_data = {"mykey": txt }
    template_name = 'login.html'
    print('forcing log out')
    return template_name, template_data


def validate_active_session(request, template_name, template_data):
    session_user_details = request.session.get('session_user_details') 
    s_login_time = request.session.get('last_clicked_on')
    session_expairy_seconds = 900
    elpsed_time_in_sec = 0
    if not (s_login_time):
        txt = "Enter user name and password to get access to  dashboard"
        template_data = {"mykey": txt }
        template_name = 'login.html' 
        print(txt)
    else:
        logged_in_time = datetime.fromtimestamp(s_login_time)
        elapsed_time = datetime.utcnow() - logged_in_time
        elpsed_time_in_sec = elapsed_time.total_seconds()
        print("logged in for sec:", elpsed_time_in_sec)
    
        if (elpsed_time_in_sec > session_expairy_seconds) :
            print('inside session  expiry block elapsed time:', elpsed_time_in_sec )
            template_name, template_data = logout(request)
        else:
            request.session['last_clicked_on'] = datetime.now().timestamp()          
            user_data = {"user_details": session_user_details }
            template_data.update(user_data)
            print('session is still active, elapsed time ', elpsed_time_in_sec)
    web_page = render(request, template_name, template_data)            
    return web_page
        

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
    
