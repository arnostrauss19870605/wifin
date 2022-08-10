from django.shortcuts import render
from urllib import request
from django.views.generic import TemplateView, ListView, DetailView, CreateView , UpdateView,FormView,DeleteView,View
from django.shortcuts import render,redirect, reverse,get_object_or_404
from django.urls import NoReverseMatch, reverse_lazy
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseRedirect
from .forms import LoginForm
from .models import *
from django.utils.http import urlencode

# Create your views here.

def test(request):
    posts = Post.objects.all()
    
    context = {
        'post': posts,
       
    }
    t = request.GET.get('Test') # => [137]
    print('This IS The ocntext : ',context)
    return render(request, 'test.html', context)


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
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        lead = form.cleaned_data
        domain = lead['domain']
        domainId = lead['domainId']

             
        print('The is the Login post : ', domain)
        #return render(request,"start.html",context)
        return redirect('landing-page',  domain = domain, domain_id = domainId ) 
        

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
       
        if 'domain' in request.GET :
            domain = request.GET['domain']
            domainId = request.GET['domainid']
            return redirect('landing-page',  domain = domain, domain_id = domainId )
        else :
             return redirect('landing-page-nop' ) 


def landing_page(request,domain,domain_id):
    
        
    if request.method == "POST" :
        # create a form instance and populate it with data from the request:
    
        print('The is the Landing post')
        #eturn render(request,"index.html",context)
        return redirect('index-page' ,  domain = domain, domain_id = domain_id) 
        

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
        context ={

           
           'form' : form

        }
       
        return render(request, "start.html", context)

def landing_page_nop(request):
    
        
    if request.method == "POST" :
        # create a form instance and populate it with data from the request:
    
       
        #eturn render(request,"index.html",context)
        return redirect('index-page-nop' ) 
        

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
        context ={

             'form' : form

        }
        print('The is the Landing GET')
        return render(request, "start.html", context)

def index(request,domain,domain_id):
    form = LoginForm(request.POST)
    
    if request.method == "POST" :
        print('The is the INDEX post')
        return redirect('interstitial-page' , domain = domain, domain_id = domain_id) 
    else :
        categories = Category.objects.all()[0:5]
        featured = Post.objects.filter(featured=True)[0:5]
        featured_other = Post.objects.filter(featured=True)[6:10]
        latest = Post.objects.order_by('-timestamp')[0:5]
        context= {
            'object_list': featured,
            'featured_other': featured_other,
            'latest': latest,
            'categories':categories,
            'domain':domain,
            'domain_id':domain_id,
      
        }
        return render(request, "index.html", context)

def index_nop(request):
    form = LoginForm(request.POST)
    
    if request.method == "POST" :
        print('The is the INDEX post')
        return redirect('interstitial-page-nop') 
    else :
        categories = Category.objects.all()[0:5]
        featured = Post.objects.filter(featured=True)[0:5]
        featured_other = Post.objects.filter(featured=True)[6:10]
        latest = Post.objects.order_by('-timestamp')[0:5]
        context= {
            'object_list': featured,
            'featured_other': featured_other,
            'latest': latest,
            'categories':categories,
           
      
        }
        return render(request, "index_nop.html", context)


 
    
  
    

def interstitial(request,domain,domain_id):
    form = LoginForm(request.POST)
   
    if request.method == "POST":


        myurl = "192.168.50.1/flash/hotspot/login2.html"  
        parameter_value_pairs = {"domain":domain,"hotspotname":domain_id}  
        req_url = myurl +  urlencode(parameter_value_pairs)
       
        print('Thjis kis the URL :',myurl)
        return redirect(req_url)

        #return render(request, 'test.html', context)
        
        #requests.post(myurl, data = {'key':'value'})
        #return render(request, 'interstitial.html', context)
    else :
        categories = Category.objects.all()[0:5]
        featured = Post.objects.filter(featured=True)[0:5]
        featured_other = Post.objects.filter(featured=True)[6:10]
        latest = Post.objects.order_by('-timestamp')[0:5]
        context= {
            'object_list': featured,
            'featured_other': featured_other,
            'latest': latest,
            'categories':categories,

        }
        
        return render(request, 'interstitial.html', context)

def interstitial_nop(request):
    form = LoginForm(request.POST)
   
    if request.method == "POST":
       
        myurl = "https://portal.wifinews.co.za/portal/index.php"  
        req_url = myurl 
       
        
        return redirect(req_url)
        #return render(request, 'interstitial.html', context)
    else :
        categories = Category.objects.all()[0:5]
        featured = Post.objects.filter(featured=True)[0:5]
        featured_other = Post.objects.filter(featured=True)[6:10]
        latest = Post.objects.order_by('-timestamp')[0:5]
        context= {
            'object_list': featured,
            'featured_other': featured_other,
            'latest': latest,
            'categories':categories,

        }
        
        return render(request, 'interstitial.html', context)
  

def post(request,slug):
    post = Post.objects.get(slug=slug)
    categories = Category.objects.all()[0:5]
    featured = Post.objects.filter(featured=True)[0:5]
    latest = Post.objects.order_by('-timestamp')[0:5]
    
    context = {
        'post': post,
        'object_list': featured,
        'latest': latest,
        'categories':categories,
            }
    return render(request, 'post_detail.html', context)

def about (request):
    return render(request, 'about_page.html')

def category_post_list (request, slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])
    context = {
        'posts': posts,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
         
    categories = Category.objects.all()[0:5]
    featured = Post.objects.filter(featured=True)[0:5]
    featured_other = Post.objects.filter(featured=True)[6:10]
    latest = Post.objects.order_by('-timestamp')[0:5]
    posts = Post.objects.order_by('-timestamp')
    context = {
        'posts': posts,
        'object_list': featured,
        'featured_other': featured_other,
        'latest': latest,
        'categories':categories,
      
    }
    return render(request, 'post_list.html', context)

