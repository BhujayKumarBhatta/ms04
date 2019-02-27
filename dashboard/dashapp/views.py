from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    txt = "Hello, guys. You're at the  index pageeeeee."
    context = {"mykey": txt }
    return render(request, 'index.html', context)
    #return HttpResponse(txt)
