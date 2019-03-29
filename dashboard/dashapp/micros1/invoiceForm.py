from django.forms import ModelForm
from dashapp.micros1.models import Invoice
from django import forms
 
class invoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['InvoiceNnumber'
                    , 'CircuitID'
                    , 'Division'
                    , 'TaxName'
                    ,'FullAddress'
                    ,'GSTNo'
                    ,'State'
                    ,'BillingDate_From'
                    ,'City'
                    ,'PremiseName'
                    ,'processing_status'
                    ,'CustomerID'
                    ,'PremiseNo'
                    ,'BillingDate_TO'
                    ,'Speed'
                    ,'Remarks'
                    ,'InvoiceDate'
                    ,'ServiceType']



class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
   