from dashapp.tokenleader import tllogin
from linkinvclient.client import LIClient
from django.shortcuts import render

    
def list_links(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        lic = LIClient(tlclient)
        list_links = lic.list_links()
        template_data = {"list_links": list_links } 
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_links))
        return result


def list_test(request):
    if request.method == 'GET': 
        _param1 = request.GET['from']
        _param2 = request.GET['name']
        response = 'You are name is :' + _param1 + ' and from :' + _param2
        return HttpResponse(response)   
