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
from dashapp.micros1 import tspinv
from dashapp.micros2 import tspdivinv

from dashapp.micros1.models import Invoice
from dashapp.micros1.invoiceForm import invoiceForm

from dashapp.micros1.invoiceForm import NameForm

from dashapp.xluploader import tspinv as xluploadertspinv
from dashapp.invstore import invoicestore


def login(request):
    result = tllogin.login(request)
    return result

 
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

def list_invoices(request):
    if 'uname' not in request.session :
      result = login(request)
    elif'uname' in request.session :
      result = tspinv.list_invoices(request)
    return result

### Divisional Invoice Functionality START
def list_divinvoices(request):
    if 'uname' not in request.session :
      result = login(request)
    elif'uname' in request.session :
      result = tspdivinv.list_divinvoices(request)
    return result

def invoicediv_delete(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:        
        result = tspdivinv.invoicediv_delete(request)    
    return result

### Divisional Invoice Functionality END
      

def invoice_create(request):
    if 'uname' not in request.session :
        result = login(request)
    else:
        result = tspinv.invoice_create(request)
    return result
 

def list_invoices_rcom(request):
    if 'uname' not in request.session :
      result = login(request)
    else:
      result = tspinv.list_invoice_rcom(request)
    return result
    
    
def invoice_delete(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:        
        result = tspinv.invoice_delete(request)    
    return result

def invoice_upload(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tspinv.invoice_upload(request)    
    return result

def invoice_dwndformat(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tspinv.downloadinvoicexlformat(request)    
    return result


def view_upload(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tspinv.view_upload(request)
    return reault

def view_update_upload(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tspinv.view_update_upload(request)
    return result

def invoice_update_upload(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tspinv.invoice_update_upload(request)    
    return result

def invoice_rcom_upload(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tspinv.invoice_rcom_upload(request)    
    return result

def invoice_approvals(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tspinv.invoice_approvals(request)    
    return result


def invoice_approve(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tspinv.invoice_approve(request)    
    return result

def invoice_reject(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tspinv.invoice_reject(request)    
    return result

def sampleinvoice(request):
    if 'uname' not in request.session :
        result = logout(request)
    else:
        result = tspinv.sampleinvoice(request)    
    return result

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

############### InvStore ###########################################
 
def invstore_list_invoices(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.list_invoices(request)
    return result 

def invstore_list_divinvoices(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.list_divinvoices(request)
    return result 

def invstore_list_invoice_bycurrent_lastorder(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.list_invoice_bycurrent_lastorder(request)
    return result

def invstore_list_invoice_byfield(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.list_invoice_byfield(request)
    return result

def invstore_invoice_delete(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.invoice_delete(request)
    return result

def invstore_list_stage1responces(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.list_stage1responces(request)
    return result

def invstore_delete_stage1responces(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.delete_stage1responces(request)
    return result

def invstore_invoice_approve(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.invoice_approve(request)
    return result

def invstore_invoice_reject(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.invoice_reject(request)
    return result
 

def invstore_invoice_rcommendations(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.invoice_rcommendations(request)
    return result

def list_invoice_divisional_invoices(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.list_divisional_invoices(request)
    return result

def invstore_invoice_update(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.invoice_update(request)
    return result

def invstore_invoice_accept(request):
    if 'uname' not in request.session :
      result = login(request)
    elif 'uname' in request.session :
      result = invoicestore.invoice_accept(request)
    return result
 
###################################################################


