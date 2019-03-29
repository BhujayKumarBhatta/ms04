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

from .forms import NameForm

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

def list_invoices_rcom(request):
    result = tspinv.list_invoice_rcom(request)
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


def list_test(request):
    result = linkv.list_test(request)  


######Invoice Model Form Testing

#def add_model(request):
 
#    if request.method == "POST":
#        form = invoiceForm(request.POST)
#        if form.is_valid():
#            model_instance = form.save(commit=False)
#            model_instance.timestamp = timezone.now()
#            model_instance.save()
#            return redirect('/')
 
#    else:
 
#        form = invoiceForm() 
#        return render(request, "invoicetemplate.html", {'form': form})



def add_model(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'invoicetemplate.html', {'form': form})
