from dashapp.tokenleader import tllogin
from linkinvclient.client import LIClient
from micros1client.client import MSClient
from django.shortcuts import render


    
def list_links(request):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)
        lic = LIClient(tlclient)
        list_links = lic.list_links()
        #template_data = {"list_links": list_links.get('message') }
        template_data = {"list_links": list_links } 
        result = render(request, 'home.html', template_data)
        #return HttpResponse(json.dumps(list_links))
        return result

################  NEW CHANGE 8 MAY 2019 ###################
###### PAYMENT
def managepayment(request):
    if request.method == 'GET': 
        #tlclient = tllogin.prep_tlclient_from_session(request)
        #lic = LIClient(tlclient)
        #list_links = lic.list_links()
        #template_data = {"list_links": list_links.get('message') }
        #result = render(request, 'managepayment.html', template_data)
        tlclient = tllogin.prep_tlclient_from_session(request)
        invClient = MSClient(tlclient) 
        list_invoices = invClient.list_invoices_clo('all','all') 
        lic = LIClient(tlclient)
        list_Lnetlink = lic.list_obj("Lnetlink","all","all")

        template_data = {"managepayment":"TRUE","list_invoices":list_invoices,"list_Lnetlink":list_Lnetlink }
        result = render(request, 'home.html',template_data)  
        return result
    if request.method == 'POST':
        payment_dict = {"invoice_id": "", "billing_from": "01-01-2019", "billing_to": "31-03-2019", "billing_type": "Installation",
        "amount": "0", "payment_date": "", "mode": "", "ref_no": "", "status": "", "netlink_id": 0}
        
        payment_dict['invoice_id'] = request.POST['invoice_id']
        payment_dict['billing_from'] = request.POST['billing_from']
        payment_dict['billing_to'] = request.POST['billing_to']
        payment_dict['billing_type'] = request.POST['billing_type']
        payment_dict['amount'] = request.POST['amount']        
        payment_dict['payment_date'] = request.POST['payment_date'] 
        payment_dict['mode'] = request.POST['mode']         
        payment_dict['ref_no'] = request.POST['ref_no']        
        payment_dict['status'] = request.POST['status']        
        payment_dict['netlink_id'] = request.POST['netlink_id']        

        tlclient = tllogin.prep_tlclient_from_session(request)
        lic = LIClient(tlclient)
        status = lic.add_payment(payment_dict)
        
        list_rate = lic.list_obj("Rate","all","all")
        list_Payment = lic.list_obj("Payment","all","all")
        list_Altaddress = lic.list_obj("Altaddress","all","all")
        list_Lnetlink = lic.list_obj("Lnetlink","all","all")
        
        template_data = {"list_rate": list_rate
                    ,"list_Payment": list_Payment
                    ,"list_Altaddress": list_Altaddress
                    ,"list_Lnetlink": list_Lnetlink,"TEST" :"Success","STATUS" : status,"listobjects":"TRUE"}
        #template_data = {"list_links": list_links,"STATUS" :status }
        result = render(request, 'home.html', template_data)                
        return result
######  RATE
def managerate(request):
    if request.method == 'GET': 
        #tlclient = tllogin.prep_tlclient_from_session(request)
        #lic = LIClient(tlclient)
        #list_links = lic.list_links()
        #template_data = {"list_links": list_links.get('message') }
        #result = render(request, 'managepayment.html', template_data)
        template_data = {"managerate":"TRUE" } 
        result = render(request, 'home.html',template_data)       
        return result
    if request.method == 'POST': 
        rate_dict = {'tsp': '', 'linktype': '', 'activity_type': '', 'otc': 0, 'rate_per_year': 0 }
        rate_dict['tsp'] = request.POST['tsp']
        rate_dict['linktype'] = request.POST['linktype']
        rate_dict['otc'] = request.POST['otc']
        rate_dict['activity_type'] = request.POST['activity_type']
        rate_dict['rate_per_year'] = request.POST['rate_per_year']        
        tlclient = tllogin.prep_tlclient_from_session(request)
        lic = LIClient(tlclient)
        status = lic.add_rate(rate_dict)  

        list_rate = lic.list_obj("Rate","all","all")
        list_Payment = lic.list_obj("Payment","all","all")
        list_Altaddress = lic.list_obj("Altaddress","all","all")
        list_Lnetlink = lic.list_obj("Lnetlink","all","all")
        
        template_data = {"list_rate": list_rate
                    ,"list_Payment": list_Payment
                    ,"list_Altaddress": list_Altaddress
                    ,"list_Lnetlink": list_Lnetlink,"TEST" :"Success","STATUS" : status,"listobjects":"TRUE"}
        
        result = render(request, 'home.html', template_data)                
        return result
        
###### ADDRESS
def manageaddress(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    lic = LIClient(tlclient)
    if request.method == 'GET': 
        template_data = {"manageaddress":"TRUE" }
        result = render(request, 'home.html',template_data)   
        return result
    if request.method == 'POST': 
        addressid = request.POST['addressid']          
        addressid = int(addressid)
## Delete only if Address ID is available and and its greater than zero
        if addressid > 0 :
            status = lic.delete_obj('Altaddress',addressid)  
        else:
## Adding New address 
            all_add = {"prem_name": "", "prem_no": 0, "state": "", "city": "", "pin": 0, "gstn": "", "sgst_rate": 0, "cgst_rate": 0}
            all_add['prem_name'] = request.POST['prem_name']
            all_add['prem_no'] = request.POST['prem_no']
            all_add['state'] = request.POST['state']
            all_add['city'] = request.POST['city']
            all_add['pin'] = request.POST['pin']        
            all_add['gstn'] = request.POST['gstn']        
            all_add['sgst_rate'] = request.POST['sgst_rate']        
            all_add['cgst_rate'] = request.POST['cgst_rate'] 
            status = lic.add_altaddress(all_add)
#Displaying all list
    list_rate = lic.list_obj("Rate","all","all")
    list_Payment = lic.list_obj("Payment","all","all")
    list_Altaddress = lic.list_obj("Altaddress","all","all")
    list_Lnetlink = lic.list_obj("Lnetlink","all","all")        
    template_data = {"list_rate": list_rate
                ,"list_Payment": list_Payment
                ,"list_Altaddress": list_Altaddress
                ,"list_Lnetlink": list_Lnetlink,"TEST" :"Success","STATUS" : status,"listobjects":"TRUE"}         
    result = render(request, 'home.html', template_data)                
    return result
             
###### LOCAL NETWORK
def managelocalnet(request):
    tlclient = tllogin.prep_tlclient_from_session(request)
    lic = LIClient(tlclient)
    if request.method == 'GET': 
        list_rate = lic.list_obj("Rate","all","all")        
        list_Altaddress = lic.list_obj("Altaddress","all","all")        
        list_links_localnet = lic.list_links()
        template_data = {"managelocalnet":"TRUE" ,"list_rate":list_rate,"list_Altaddress":list_Altaddress,"list_links_localnet":list_links_localnet}
        result = render(request, 'home.html',template_data)     
        return result
    if request.method == 'POST':
        netlink_id = request.POST['netlink_id']          
        netlinkid = int(netlink_id)
        if netlinkid > 0 :
            status = lic.delete_obj('Lnetlink',netlinkid)  
        else:
            lnet_d = {"infoopsid": "", "altaddress_id": 0, "rate_id": 0, "last_payment_date": ""}
            lnet_d['infoopsid'] = request.POST['infoopsid_id']
            lnet_d['altaddress_id'] = request.POST['altaddress_id']
            lnet_d['rate_id'] = request.POST['rate_id']
            lnet_d['last_payment_date'] = request.POST['last_payment_date']
            status = lic.add_lnetlink(lnet_d)            
    list_rate = lic.list_obj("Rate","all","all")
    list_Payment = lic.list_obj("Payment","all","all")
    list_Altaddress = lic.list_obj("Altaddress","all","all")
    list_Lnetlink = lic.list_obj("Lnetlink","all","all")        
    template_data = {"list_rate": list_rate
                ,"list_Payment": list_Payment
                ,"list_Altaddress": list_Altaddress
                ,"list_Lnetlink": list_Lnetlink,"TEST" :"Success","STATUS" : status,"listobjects":"TRUE"}
    result = render(request, 'home.html', template_data)                
    return result
###### LIST ALL
def listobjects(request):
    #if request.method == 'GET':
    tlclient = tllogin.prep_tlclient_from_session(request)
    lic = LIClient(tlclient)
    list_rate = lic.list_obj("Rate","all","all")
    list_Payment = lic.list_obj("Payment","all","all")
    list_Altaddress = lic.list_obj("Altaddress","all","all")
    list_Lnetlink = lic.list_obj("Lnetlink","all","all")

    template_data = {"list_rate": list_rate
                    ,"list_Payment": list_Payment
                    ,"list_Altaddress": list_Altaddress
                    ,"list_Lnetlink": list_Lnetlink,"TEST" :"Success","listobjects":"TRUE"}
    result = render(request, 'home.html', template_data)
    #template_data = {"listobjects":"TRUE" }
    #result = render(request, 'home.html',template_data)
    return result


def getallobjects(self):
    
    tlclient = tllogin.prep_tlclient_from_session(request)
    lic = LIClient(tlclient)
    list_rate = lic.list_obj("Rate","all","all")
    list_Payment = lic.list_obj("Payment","all","all")
    list_Altaddress = lic.list_obj("Altaddress","all","all")
    list_Lnetlink = lic.list_obj("Lnetlink","all","all")

    template_data = {"list_rate": list_rate
                    ,"list_Payment": list_Payment
                    ,"list_Altaddress": list_Altaddress
                    ,"list_Lnetlink": list_Lnetlink,"TEST" :"Success"}
    return template_data
    #if request.method == 'POST':
    #    lnet_d = {"infoopsid": "", "altaddress_id": 0, "rate_id": 0,
    #    "last_payment_date": "01-04-2019"}
    #    lnet_d['altaddress_id'] = request.POST['altaddress_id']
    #    lnet_d['rate_id'] = request.POST['rate_id']
    #    lnet_d['last_payment_date'] = request.POST['last_payment_date']
            
    #    tlclient = tllogin.prep_tlclient_from_session(request)
    #    lic = LIClient(tlclient)
    #    status = lic.add_lnetlink(lnet_d)
    #    template_data = {"list_links":
    #    list_links.get('message'),"LOCALNET_STATUS" :status }
    #    result = render(request, 'list_links.html', template_data)
    #    return result

#############################################################
def list_test(request):
    if request.method == 'GET': 
        _param1 = request.GET['from']
        _param2 = request.GET['name']
        response = 'You are name is :' + _param1 + ' and from :' + _param2
        return HttpResponse(response)   
