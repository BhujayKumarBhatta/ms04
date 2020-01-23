
from clienttelegraph.client import clienttelegraph
from dashapp.tokenleader import tllogin
from dashapp.tokenleader.tllogin import validate_active_session, validate_token_n_session


@validate_token_n_session()
def create_mailmap(request):
    tlclient = tllogin.prep_tlclient_from_session(request)        
    telegclient=clienttelegraph(tlclient)
    if request.method == 'GET': 
        template_name = "telegraph/create_mailmap.html"
        template_data = {}
    if request.method == 'POST':
        must_have = ["status_name", "docid", "list_of_recpt_org", ]
        for m in must_have:
            if m not in request.POST:
                status = "form has not been filled up with all necessary data" 
        map_data = {"status_name": request.POST.get('status_name'),
                    "docid": request.POST.get('docid'),
                    "list_of_recpt_org": request.POST.get('list_of_recpt_org'),
                    }
        status = telegclient.create_mailmap(map_data)
        template_name = "wanlinks/exec_status.html"
        template_data = {"status": status }
    web_page = validate_active_session(request, template_name, template_data)
    return web_page

@validate_token_n_session()
def list_mailmap(request, status_name=None, docid=None):
    if request.method == 'GET': 
        tlclient = tllogin.prep_tlclient_from_session(request)        
        telegclient=clienttelegraph(tlclient)
        mail_map_all =[]
        mail_map_by_status_or_id = {}
        template_name = "telegraph/mailmap_detail.html"
        if status_name and status_name == 'all':
            mail_map_all = telegclient.list_mailmap_bystatus('all')
            template_name = "telegraph/mailmap_list.html"
        elif status_name and status_name != 'all':
            mail_map_by_status_or_id = telegclient.list_mailmap_bystatus(status_name)
        if docid:
            mail_map_by_status_or_id = telegclient.list_mailmap_bydocid(docid)
        template_data = {"mail_map_all": mail_map_all, 
                         "mail_map_by_status_or_id": mail_map_by_status_or_id}
        web_page = validate_active_session(request, template_name, template_data)
        return web_page 
         
 
#                
# @validate_token_n_session()    
# def delete_events(request):
#     tlclient = tllogin.prep_tlclient_from_session(request)
#     penclient=clientpenman(tlclient)
#     status = None
#     if request.method == 'POST':
#         invoicenum = request.POST['invoiceno']          
#         #invoiceno = int(invoicenum)
#         if invoicenum  and len(invoicenum)  > 0 and invoicenum !='all':
#             status = penclient.delete_events(invoicenum)
#             print('received delete for invoice number ?', invoicenum)        
#         elif invoicenum =='all':
#             print('going to delete all ....')
#             status = penclient.delete_events('all') 
#             
#     list_events = penclient.list_events('all')  
#     action_buttons = ["DeleteAllInvoiceEvents"]
#     template_name = 'admin_pages/list_events.html'
#     template_data = {"Penman_list_events": list_events,
#                           "action_buttons": action_buttons, 
#                           "delete_status" :status }
#     web_page = validate_active_session(request, template_name, template_data)
#     return web_page
# 
# 
# 
# @validate_token_n_session()    
# def delete_event(request):
#     tlclient = tllogin.prep_tlclient_from_session(request)
#     penclient=clientpenman(tlclient)
#     status = None
#     invoicenum = ""
#     event_id = ""
#     test = ""
#     
#     if request.method == 'POST':
#         invoicenum = request.POST['invoiceno']
#         event_id = request.POST['event_id']
#         if invoicenum  and len(invoicenum)  > 0 and event_id  and len(event_id)  > 0:
#             status = penclient.delete_events_by_id(invoicenum, event_id)
#             test = "test-------------"
#                         
#     list_events = penclient.list_events('all')  
#     action_buttons = ["DeleteAllInvoiceEvents"]
#     template_name = 'admin_pages/list_events.html'
#     template_data = {"Penman_list_events": list_events,
#                           "action_buttons": action_buttons, 
#                           "delete_status" :status , "invoicenum": invoicenum
#                           , "event_id" : event_id
#                           ,"test": test}
#     web_page = validate_active_session(request, template_name, template_data)
#     return web_page
# 
#     
#     
   