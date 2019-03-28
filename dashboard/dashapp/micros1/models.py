from django.db import models
from dashapp.micros1.models import Invoice


class Invoice(models.Model):

    InvoiceNnumber = models.CharField(max_length=500)
    CircuitID = models.IntegerField(default=0)
    Division = models.CharField(max_length=200)
    TaxName  = models.CharField(max_length=500)
    FullAddress =  models.CharField(max_length=2000)
    GSTNo =   models.CharField(max_length=500)
    State = models.CharField(max_length=500)
    BillingDate_From  = models.DateTimeField(auto_now=True)
    City = models.CharField(max_length=500)
    PremiseName = models.CharField(max_length=500)
    processing_status = models.CharField(max_length=500)
    CustomerID = models.CharField(max_length=500)
    PremiseNo = models.CharField(max_length=500)
    BillingDate_TO = models.DateTimeField(auto_now=True)
    Speed = models.CharField(max_length=500)
    Remarks = models.CharField(max_length=2000)
    InvoiceDate = models.DateTimeField(auto_now=True)
    ServiceType = models.CharField(max_length=500)



    def __unicode__(self):
        return '{0}'.format(self.content)
