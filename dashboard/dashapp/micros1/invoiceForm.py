from django.forms import ModelForm
from myapp.models import Invoice
 
class invoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['InvoiceNnumber', 'CircuitID', 'Division', 'TaxName']