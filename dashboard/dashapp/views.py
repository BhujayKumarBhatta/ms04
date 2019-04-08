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

from dashapp.micros1.models import Invoice
from dashapp.micros1.invoiceForm import invoiceForm

from dashapp.micros1.invoiceForm import NameForm

def login(request):
    result = tllogin.login(request)
    return result


def list_links(request):
    result = linkv.list_links(request)
    return result


def list_org(request):
    result = tlviews.list_org(request)
    return result


def list_ou(request):
    result = tlviews.list_ou(request)
    return result


def list_dept(request):
    result = tlviews.list_dept(request)
    return result

def list_role(request):
    result = tlviews.list_role(request)
    return result


def list_users(request):
    result = tlviews.list_users(request)
    return result


def adduser(request):
    result = tlviews.adduser(request)
    return result


def list_invoices(request):
    result = tspinv.list_invoices(request)
    return result

def invoice_create(request):
    result = tspinv.invoice_create(request)
    return result
 

def list_invoices_rcom(request):
    result = tspinv.list_invoice_rcom(request)
    return result
    
    
def invoice_delete(request):
    result = tspinv.invoice_delete(request)    
    return result

def invoice_upload(request):
    result = tspinv.invoice_upload(request)    
    return result


def view_upload(request):
    result = tspinv.view_upload(request)
    return reault

def view_update_upload(request):
    result = tspinv.view_update_upload(request)
    return result

def invoice_update_upload(request):
    result = tspinv.invoice_update_upload(request)    
    return result

def invoice_rcom_upload(request):
    result = tspinv.invoice_rcom_upload(request)    
    return result

def invoice_approvals(request):
    result = tspinv.invoice_approvals(request)    
    return result


def invoice_approve(request):
    result = tspinv.invoice_approve(request)    
    return result

def invoice_reject(request):
    result = tspinv.invoice_reject(request)    
    return result

def sampleinvoice(request):
    result = tspinv.sampleinvoice(request)    
    return result


def list_test(request):
    result = linkv.list_test(request)  


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



 
