from django.db import models
from .sms import send_my_sms
from django.db.models import Max
from django.core.exceptions import ValidationError
from crum import get_current_user
from django.utils import timezone
from wifi_app.models import CustomUser

def validate_length(value,length=10):
    if len(str(value))!=length:
        raise ValidationError(u'%s number needs to be 10 digits e.g 0726124698' % value)

# Create your models here.

class VoucherType(models.Model):
    description  = models.CharField(max_length=20)
   
    def __str__(self):
        return f"{self.description} "

class Voucher(models.Model):
    company_name  = models.CharField(max_length=200)
    voucher_type = models.ForeignKey(VoucherType, on_delete=models.SET_NULL, null=True,  blank=True,verbose_name = "Voucher Type")
    sell_price = models.CharField(max_length=20 , null=True,  blank=True,)
    card_code = models.CharField(max_length=20 , null=True,  blank=True,)
    language = models.CharField(max_length=2 , null=True,  blank=True,)
    hs_domian_data_id = models.CharField(max_length=10, null=True,  blank=True,)
      
    date_created = models.DateTimeField('date created')
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.voucher_type} "

class Location(models.Model):
    location_Description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.location_Description} "
   
class Activation(models.Model):
    location = models.CharField(max_length=200,  null=True,  blank=True)
    voucher_type = models.ForeignKey(VoucherType, on_delete=models.SET_NULL, null=True,  blank=True,verbose_name = "Voucher Type")
    cell_number = models.CharField(max_length=10,validators=[validate_length])
    date_sent = models.DateTimeField(null=True, blank=True, verbose_name = "Date Activated")

    def __str__(self):
        return f"{self.location} - {self.cell_number} "

    def save(self, *args, **kw): 
      
        mydata = Voucher.objects.all().values().filter(activated = False,voucher_type = self.voucher_type)[0]
        the_id = mydata['id']
        the_voucher = mydata['card_code']
       
        send_my_sms(self.cell_number,the_voucher)   

        obj = Voucher.objects.get(pk=the_id)
        obj.activated = True
        obj.save()

        user =   get_current_user()  
        user_pk = user.pk
        obj_1 = CustomUser.objects.get(pk=user_pk)

        self.location = obj_1.site

        if self.date_sent is None:
            self.date_sent = timezone.localtime(timezone.now())
      
        super(Activation, self).save(*args, **kw)
  
