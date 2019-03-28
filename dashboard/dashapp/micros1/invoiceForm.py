from django.forms import ModelForm
from dashapp.micros1.models import Invoice
 
class invoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['InvoiceNnumber', 'CircuitID', 'Division', 'TaxName']