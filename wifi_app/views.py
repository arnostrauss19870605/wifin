from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView , UpdateView,FormView,DeleteView,View
from django.shortcuts import render,redirect, reverse,get_object_or_404
from django.urls import NoReverseMatch, reverse_lazy
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseRedirect
from .forms import LoginForm

# Create your views here.


class LandingPageview(TemplateView) :

    #template_name = "landing.html"
    template_name = "start.html"

class LoginPageview(TemplateView) :
    #template_name = "landing.html"
    template_name = "login.html"

class IndexPageview(TemplateView) :

    template_name = "index.html"

class InterstitialPageview(TemplateView) :

    template_name = "interstitial.html"

class Login_mahalaPageview(TemplateView) :

    template_name = "login_mahala.html"

def login_page(request):
    form = LoginForm(request.POST)
    if request.method == "POST" and form.is_valid():
        # create a form instance and populate it with data from the request:
        data = form.cleaned_data
        #domain = data['domain']
       

        context ={

            'data' : data,

        }
       
        return render(request,"start.html",context)
        

    # if a GET (or any other method) we'll create a blank form
    else:
        context ={}
        context['form']= LoginForm()
        return render(request, "login.html", context)


