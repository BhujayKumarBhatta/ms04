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
        def clean(self):
            cleaned_data = super(invoiceForm, self).clean()
            Division = cleaned_data.get('Division')
            TaxName = cleaned_data.get('TaxName')
            GSTNo = cleaned_data.get('GSTNo')
            if len(TaxName) < 5: 
                self._errors['TaxName'] = self.error_class([ 
                    'Minimum 5 characters required']) 

            if not Division and not TaxName and not GSTNo:
                raise forms.ValidationError('Need to write error messages accordingly.')



class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
   