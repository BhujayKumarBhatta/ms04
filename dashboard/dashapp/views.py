import os
import json
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
#File Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from werkzeug.utils import secure_filename

from dashapp.tokenleader import tllogin
from dashapp.linkinv import linkinv_views as linkv
from dashapp.tokenleader import tlviews

from dashapp.xluploader import tspinv as xluploadertspinv

from dashapp.penman import penman
from dashapp.paperhouse import paperhouse
from dashapp.striker import striker


def login(request):
    result = tllogin.login(request)
    return result

def log_out(request):
    print("i m inside lout out view")
    template_name, template_data  = tllogin.logout(request)
    return render(request, template_name, template_data)
    
# def home(request):
#     session_user_details = request.session.get('session_user_details')
#     template_data = {"user_details": session_user_details }   
#     result = render(request, 'home.html', template_data)            
#     return result
 
def list_links(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = linkv.list_links(request)
    return result
    
def managepayment(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = linkv.managepayment(request)
    return result

def managerate(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = linkv.managerate(request)
    return result

def manageaddress(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = linkv.manageaddress(request)
    return result

def managelocalnet(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = linkv.managelocalnet(request)
    return result

def listobjects(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = linkv.listobjects(request)
    return result

# TOKENLEADER ======================================

def list_org(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.list_org(request)
    return result
    		
def add_org(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.add_org(request)
    return result
    		
def delete_org(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.delete_org(request)
    return result       			

def list_ou(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.list_ou(request)
    return result

def add_ou(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.add_ou(request)
    return result   
    		
def delete_ou(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.delete_ou(request)
    return result    

def list_dept(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.list_dept(request)
    return result
    		
def add_dept(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.add_dept(request)
    return result
    		    		
def delete_dept(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.delete_dept(request)
    return result  
    		
def list_role(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.list_role(request)
    return result

def add_role(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.add_role(request)
    return result
    		
def delete_role(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.delete_role(request)
    return result


def list_users(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.list_users(request)
    return result

def adduser(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.adduser(request)
    return result
    		
def delete_user(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.delete_user(request)
    return result
    		
def list_wfc(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.list_wfc(request)
    return result

def add_wfc(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.add_wfc(request)
    return result
    		
def delete_wfc(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.delete_wfc(request)
    return result
    		
# TOKENLEADER ===========================================



### Divisional Invoice Functionality END
      




def add_service(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.add_service(request)    
    return result

def list_service(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.list_service(request)    
    return result

def delete_service(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tlviews.delete_service(request)    
    return result


def list_test(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = linkv.list_test(request)  

def home2(request):
    result = render(request, 'home3.html')
    return result

#### Log out
def logout(request):
    if request.session.has_key('uname'):
        del request.session['uname']
    if request.session.has_key('psword'):
        del request.session['psword']
    request.session.clear_expired() 
    result = tllogin.login(request)
    return result
    #result = render(request, "login.html", {'SESSION_EXPIRE':'TRUE'})
    #return result  

######Invoice Model Form Testing
def add_model(request):
 
    if request.method == "POST":
        form = invoiceForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/') 
    else: 
        form = invoiceForm() 
        return render(request, "home.html", {'CREATE_INVOICE_FORM': form})

 
############### Xluploader #########################################


def xluploader_invoice_upload(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = xluploadertspinv.invoice_upload(request)    
    return result

############################# PEN and PAPER House#######################################

def penman_list_events(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = penman.list_events(request)
    return result

def penman_delete_events(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = penman.delete_events(request)
    return result



def paperhouse_list_invoice(request, listype):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
        if listype == 'admin':
            result = paperhouse.list_invoices(request, 'admin')
        else:
            result = paperhouse.list_invoices(request)
    return result

# def paperhouse_list_invoice_admin(request):
#     if 'uname' not in request.session :
#       result = login(request)
#     elif 'uname' in request.session :
#       result = paperhouse.list_invoices(request, "admin")
#     return result 

def paperhouse_delete_invoice(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = paperhouse.delete_invoices(request)
    return result

def tsp_list_invoice(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = paperhouse.tsp_list_invoices(request)
    return result


def striker_list_responces(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = striker.list_responces(request)
    return result


def striker_delete_responces(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = striker.delete_responces(request)
    return result

###################################################################



