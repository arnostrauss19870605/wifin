from django.db import models
from .sms import send_my_sms
from django.db.models import Max
from django.core.exceptions import ValidationError

def validate_length(value,length=10):
    if len(str(value))!=length:
        raise ValidationError(u'%s number needs to be 10 digits e.g 0726124698' % value)

# Create your models here.

class Voucher(models.Model):
    voucher_text = models.CharField(max_length=200)
    date_created = models.DateTimeField('date created')
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.voucher_text} "

class Location(models.Model):
    location_Description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.location_Description} "
   
class Activation(models.Model):
    location = models.CharField(max_length=200,  null=True,  blank=True)
    cell_number = models.CharField(max_length=10,validators=[validate_length])
    date_sent = models.DateTimeField(null=True, blank=True, verbose_name = "Date Activated")

    def __str__(self):
        return f"{self.location} - {self.cell_number} "

    def save(self, *args, **kw): 
        #the_voucher = Voucher.objects.filter(activated = False).values_list('voucher_text',flat=True)[0]

        mydata = Voucher.objects.all().values().filter(activated = False)[0]
        the_id = mydata['id']
        the_voucher = mydata['voucher_text']
       
        send_my_sms(self.cell_number,the_voucher)   

        obj = Voucher.objects.get(pk=the_id)
        obj.activated = True
        obj.save()

        super(Activation, self).save(*args, **kw)
  
