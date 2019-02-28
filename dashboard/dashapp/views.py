from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from tokenleaderclient.configs.config_handler import Configs    
from  tokenleaderclient.client.client import Client 
from micros1client.client   import MSClient


tlclient = None
# c = MSClient(tlclient)


# Create your views here.
def index(request):
    if request.method == 'GET':
        txt = "Hello, guys. You're at the  index pageeeeee."
        context = {"mykey": txt }
        return render(request, 'index.html', context)
    elif request.method == 'POST':
        uname = request.POST.get('username', '')
        psword = request.POST.get('password', '')
        auth_config = Configs(uname, psword )
        tlclient = Client(auth_config)
        return HttpResponse(tlclient.gettoken())
    #return HttpResponse(txt)


    
