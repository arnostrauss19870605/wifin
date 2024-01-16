"""Declare models for YOUR_APP app."""
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.urls import reverse
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from vouchers.sms import send_my_notification_sms
from django.utils.translation import gettext_lazy as _


DURATION_CHOICES = (
    ('1',1),
    ('3', 3),
    ('6',6),
    ('12',12),
    ('24',24),
    ('48',48),
    ('96',96),
)

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    site=models.CharField(max_length=40,null=True, blank=True)
    
  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Category(models.Model):
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=20)
    slug = models.SlugField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    myfield = MarkdownxField( null=True, blank=True)

    @property
    def formatted_markdown(self):
        return markdownify(self.myfield)   

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', args=[str(self.slug)])


# post model
class Topic(models.Model):
       
    # added after get_absolute_url function
    # to get comment with parent is none and active is true, we can use this in template
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    title = models.CharField(max_length=250,default='')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.CharField(max_length=250,default='')
    body = models.TextField(default='')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title


    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

    def get_absolute_url(self):
        return reverse('topic', args=[str(self.slug)])

def validate_length(value,length=10):
    if len(str(value))!=length:
        raise ValidationError(u'%s number needs to be 10 digits e.g 0726124698' % value)

# comment model    
class Comment(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE, related_name="comments")
    name=models.CharField(max_length=50)
    email=models.EmailField()
    cell_number = models.CharField(max_length=10,validators=[validate_length])
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField(max_length=350)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    notify = models.BooleanField(default=False)
 

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f"{self.body} "

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)

    def save(self, *args, **kw): 
      
        try : 
            obj = Comment.objects.get(pk=self.parent_id)
            the_parent_cell_number = obj.cell_number
            parent_notification = obj.notify
            the_date_created = obj.created
            future_date = the_date_created + datetime.timedelta(days=7)
            if parent_notification == True  : 
                send_my_notification_sms(the_parent_cell_number,self.parent_id)
                print('The Time',future_date)

              
            super(Comment, self).save(*args, **kw)
        except :
            

            super(Comment, self).save(*args, **kw)


#https://dev.to/yahaya_hk/how-to-populate-your-database-with-data-from-an-external-api-in-django-398i
class Registered_User(models.Model):
    hsDomainsDataID =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Domain Data ID")
    hsUsersID =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "User ID")
    username =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Username")
    first_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Firstname")
    last_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Lastname")
    email =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Email Address")
    mobile_phone =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Mobile Phone")
    address =  models.CharField(blank=True, null=True,max_length=400,verbose_name = "Address")
    city =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "City")
    state =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "State")
    zip =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Zip")
    country =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Country")
    gender =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Gender")
    date_created =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Creation Date")
    language =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Language")
    year_of_birth =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Year Of Birth")
    month_of_birth =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Month Of Birth")
    day_of_birth =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Day Of Birth")
    reseller_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Reseller Company Name")
    manager_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Manager Company Name")
    domain_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Domain Name")
    expiration_date =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Expiration Date")
    product =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Product Description")
    hs_product_id =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Product ID")
    last_transaction_date =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Last Transaction Date")
    date_imported = models.DateTimeField(blank=True, null=True,verbose_name = "Date Imported")
    uploaded = models.BooleanField(default=False,verbose_name = "Upload Status")
    status_descript =  models.CharField(blank=True, null=True,max_length=1000,verbose_name = "Status Description")
    payload = models.JSONField(blank=True,null=True)
    date_uploaded = models.DateTimeField(blank=True, null=True,verbose_name = "Date Uploaded")


    def __str__(self):
        return f"{self.hsDomainsDataID} : {self.first_name} - {self.last_name} "
    
    def save(self, *args, **kwargs):
        if self.date_imported is None:
            self.date_imported = timezone.localtime(timezone.now())

        super(Registered_User, self).save(*args, **kwargs)  

class Country(models.Model):
    country_code =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Country Code")
    country_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Country Name")

class Domain(models.Model):
    description =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Description")
    domain_id =  models.CharField(blank=True, null=True,max_length=15,verbose_name = "Domain ID")
    url =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Captive Portal API URL")
    endpoint =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Captive Portal API Endpoint")
    api_key =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Captive Portal API Key")
    api_seceret =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Captive Portal API Secret")
    last_extracted_date = models.DateTimeField(blank=True, null=True,verbose_name = "Date Last Extracted From")
    omnisend_url =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Omnisend URL")
    omnisend_endpoint =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Omnisend Endpoint")
    omnisend_api_key =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Omnisend API Key")
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.description} - {self.domain_id} "
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())

        self.last_updated = timezone.localtime(timezone.now())  

        super(Domain, self).save(*args, **kwargs)

class Survey_settings(models.Model):
    description =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Description")
    domain_id =  models.CharField(blank=True, null=True,max_length=15,verbose_name = "Domain ID")
    survey_id =  models.CharField(blank=True, null=True,max_length=15,verbose_name = "Survey ID")
    creation_date = models.DateTimeField(blank=True, null=True,verbose_name = "Creation Date")
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.description} - {self.survey_id} "
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())

        self.last_updated = timezone.localtime(timezone.now())  

        super(Survey_settings, self).save(*args, **kwargs)

class Domain_User(models.Model):
    user_id =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Description")
    domain_id =  models.CharField(blank=True, null=True,max_length=15,verbose_name = "Domain ID")
    last_extracted_date = models.DateTimeField(blank=True, null=True,verbose_name = "Date Last Extracted From")
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    extracted = models.BooleanField(default=False,verbose_name = "Extracted Status")

    def __str__(self):
        return f"{self.user_id} : {self.domain_id}  "
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())

        self.last_updated = timezone.localtime(timezone.now())  

        super(Domain_User, self).save(*args, **kwargs)



class Core_Quiz(models.Model):
    reseller_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Reseller Company Name")
    manager_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Manager Company Name")
    domain_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Domain Name")
    insertion_date = models.DateTimeField(blank=True, null=True,verbose_name = "Insertion Date ")
    question_type =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question Type")
    surveyID =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Survey ID")
    hsUsersID =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "User ID")
    username =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Username")
    first_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Firstname")
    last_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Lastname")
    company_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Company Name")
    city =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "City")
    address =  models.CharField(blank=True, null=True,max_length=400,verbose_name = "Address")
    zip =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Zip")
    state =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "State")
    country =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Country")
    gender =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Gender")
    year_of_birth =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Year Of Birth")
    month_of_birth =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Month Of Birth")
    day_of_birth =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Day Of Birth")
    room_or_site =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Room Or Site")
    hs_product_id =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Product ID")
    email =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Email Address")
    phone =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Phone")
    mobile_phone =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Mobile Phone")
    conditions_accepted =  models.CharField(blank=True, null=True,max_length=10,verbose_name = "Conditions Accepted")
    privacy_policyAccepted =  models.CharField(blank=True, null=True,max_length=10,verbose_name = "Privacy PolicyAccepted")
    marketing_accepted =  models.CharField(blank=True, null=True,max_length=10,verbose_name = "Marketing Accepted")
    newsletters_accepted =  models.CharField(blank=True, null=True,max_length=10,verbose_name = "Newsletters Accepted")
    q_1 =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question 1")
    q_2 =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question 2")
    q_3 =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question 3")
    q_4 =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question 4")
    q_5 =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question 5")
    score =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Score")
    
    date_imported = models.DateTimeField(blank=True, null=True,verbose_name = "Date Imported")
    uploaded = models.BooleanField(default=False,verbose_name = "Upload Status")
    status_descript =  models.CharField(blank=True, null=True,max_length=1000,verbose_name = "Status Description")
    payload = models.JSONField(blank=True,null=True)
    date_uploaded = models.DateTimeField(blank=True, null=True,verbose_name = "Date Uploaded to API")

    consolidated = models.BooleanField(default=False)
    date_consolidated = models.DateTimeField(blank=True, null=True,verbose_name = "Date Consolidated")
    
    personal_info = models.BooleanField(default=False)
    date_personal_info = models.DateTimeField(blank=True, null=True,verbose_name = "Date Personal Info Updated")
    domain_id =  models.CharField(blank=True, null=True,max_length=15,verbose_name = "Domain ID")
    date_extracted = models.DateTimeField(blank=True, null=True,verbose_name = "Date Extracted From Captive Portal")



    def __str__(self):
        return f"{self.surveyID} : {self.first_name} - {self.last_name} "
    
    def save(self, *args, **kwargs):
        if self.date_imported is None:
            self.date_imported = timezone.localtime(timezone.now())

        super(Core_Quiz, self).save(*args, **kwargs)  

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
  
class Consolidated_Core_Quiz(models.Model):
    reseller_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Reseller Company Name")
    manager_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Manager Company Name")
    domain_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Domain Name")
    insertion_date = models.DateTimeField(blank=True, null=True,verbose_name = "Insertion Date ")
    question_type =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question Type")
    surveyID =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Survey ID")
    hsUsersID =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "User ID")
    username =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Username")
    first_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Firstname")
    last_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Lastname")
    company_name =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Company Name")
    city =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "City")
    address =  models.CharField(blank=True, null=True,max_length=400,verbose_name = "Address")
    zip =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Zip")
    state =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "State")
    country =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Country")
    gender =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Gender")
    year_of_birth =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Year Of Birth")
    month_of_birth =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Month Of Birth")
    day_of_birth =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Day Of Birth")
    room_or_site =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Room Or Site")
    hs_product_id =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Product ID")
    email =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Email Address")
    phone =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Phone")
    mobile_phone =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Mobile Phone")
    conditions_accepted =  models.CharField(blank=True, null=True,max_length=10,verbose_name = "Conditions Accepted")
    privacy_policyAccepted =  models.CharField(blank=True, null=True,max_length=10,verbose_name = "Privacy PolicyAccepted")
    marketing_accepted =  models.CharField(blank=True, null=True,max_length=10,verbose_name = "Marketing Accepted")
    newsletters_accepted =  models.CharField(blank=True, null=True,max_length=10,verbose_name = "Newsletters Accepted")
    q_1 =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question 1")
    q_2 =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question 2")
    q_3 =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question 3")
    q_4 =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question 4")
    q_5 =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Question 5")
    score =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Score")
    date_consolidated = models.DateTimeField(blank=True, null=True,verbose_name = "Date Consolidated")

    status_descript =  models.JSONField(blank=True, null=True,verbose_name = "Status Description")
    status_check = models.BooleanField(default=False)
    payload = models.JSONField(blank=True,null=True)
    date_uploaded = models.DateTimeField(blank=True, null=True,verbose_name = "Date Uploaded to API")
    upload_required = models.BooleanField(default=False)
    uploaded = models.BooleanField(default=False)
    product =  models.CharField(blank=True, null=True,max_length=100,verbose_name = "Interested Product")

    def __str__(self):
        return f"{self.surveyID} : {self.first_name} - {self.last_name} "
    
    def save(self, *args, **kwargs):
        if self.date_consolidated is None:
            self.date_consolidated = timezone.localtime(timezone.now())
            if safe_int(self.q_1) == 1 :
                if 18 <= safe_int(self.q_2) <= 20 :
                    
                    if safe_int(self.q_3) == 6 :

                        if 10 <= safe_int(self.q_5) <= 12 :
                            self.upload_required = True
                            self.product = "Medical Insurance"
                        

        
        super(Consolidated_Core_Quiz, self).save(*args, **kwargs)  

class Upload_Interval(models.Model):
    interval =  models.CharField(blank=True,null=True,max_length=3,choices=DURATION_CHOICES,default=24)

    def __str__(self):
        return f"Set Inerval : {self.interval}"
    


   

  
