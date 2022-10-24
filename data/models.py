"""Declare models for YOUR_APP app."""
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.urls import reverse
import uuid
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Log(models.Model):
   
    utm_1 = models.TextField(null=True, blank=True)
    utm_2 = models.TextField(null=True, blank=True)
    utm_3 = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    page = models.TextField(null=True, blank=True)
    counter = models.IntegerField(default=0)
    session = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.utm_1} {self.utm_2} - {self.page} - - {self.timestamp}"

    def get_absolute_url(self):
        return reverse('log', args=[str(self.id)])
