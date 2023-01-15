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
import uuid
from django.utils.translation import gettext_lazy as _



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
            obj = Comment.objects.get(pk=self.parent_id)
            the_parent_cell_number = obj.cell_number
            parent_notification = obj.notify
            the_date_created = obj.created
            future_date = the_date_created + datetime.timedelta(days=7)          
            print('The Time 2 :',future_date)

            super(Comment, self).save(*args, **kw)

  
