from django.shortcuts import render
from urllib import request
from django.views.generic import TemplateView, ListView, DetailView, CreateView , UpdateView,FormView,DeleteView,View
from django.shortcuts import render,redirect, reverse,get_object_or_404
from django.urls import NoReverseMatch, reverse_lazy
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseRedirect
from .forms import LoginForm
from .models import *
from data.models import *
from django.utils.http import urlencode

# Create your views here.

def test(request):
    posts = Post.objects.all()
    
    context = {
        'post': posts,
       
    }
    t = request.GET.get('Test') # => [137]
   
    myurl = "http://192.168.50.1/flash/hotspot/login2.html" 
    print('This IS The ocntext : ',context)
    #return redirect(myurl)

    return render(request, "test.html", context)


class LoginPageview(TemplateView) :
    #template_name = "landing.html"
    template_name = "login.html"


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

             
       
        #return render(request,"start.html",context)
        #return redirect('landing-page',  domain = domain, domain_id = domainId ) 
        return redirect( f"{reverse('landing-page')}?{urlencode({'next': 'nextos' })}")
        

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
       
        if 'utm_source' in request.GET and 'utm_medium' in request.GET and 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
          
            
            #return redirect('landing-page',  domain = domain, domain_id = domainId )
            return redirect( f"{reverse('landing-page')}?{urlencode({'utm_source': utm_source })}&{urlencode({'utm_medium': utm_medium })}&{urlencode({'utm_campaign': utm_campaign })}")
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
             return render(request, "exit_index.html", context)
             

def landing_page(request):

    print("LAnding Request Method :" , request.method )
    
        
    if request.method == "POST" :
        # create a form instance and populate it with data from the request:
    
        
        #eturn render(request,"index.html",context)
        if 'utm_source' in request.GET and 'utm_medium' in request.GET and 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            the_session = request.session.session_key
            
            data_entry = Log(utm_1=utm_source,utm_2=utm_medium,utm_3=utm_campaign,page='landing',counter=1,session = the_session )
            data_entry.save()
            
            #return redirect('landing-page',  domain = domain, domain_id = domainId )
            return redirect( f"{reverse('landing-page-1')}?{urlencode({'utm_source': utm_source })}&{urlencode({'utm_medium': utm_medium })}&{urlencode({'utm_campaign': utm_campaign })}")
        else :
            the_session = request.session.session_key
            data_entry = Log(utm_1='Unknown',utm_2='Unknown',utm_3='Unknown',page='landing',counter=1,session = the_session)
            data_entry.save()
            return redirect('landing-page-1') 
        

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
        context ={

           
           'form' : form

        }
       
        return render(request, "start.html", context)

def landing_page_1(request):
    print("Landing 1 Request Method :" , request.method )
        
    if request.method == "POST" :
       

        if 'utm_source' in request.GET and 'utm_medium' in request.GET and 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            the_session = request.session.session_key

            data_entry = Log(utm_1=utm_source,utm_2=utm_medium,utm_3=utm_campaign,page='landing_1',counter=1,session = the_session)
            data_entry.save()

            return redirect('home-page') 
           # return redirect( f"{reverse('index-page')}?{urlencode({'utm_source': utm_source })}&{urlencode({'utm_medium': utm_medium })}&{urlencode({'utm_campaign': utm_campaign })}")
        else :
            the_session = request.session.session_key
            data_entry = Log(utm_1='Unknown',utm_2='Unknown',utm_3='Unknown',page='landing_1',counter=1,session = the_session)
            data_entry.save()

            return redirect('home-page') 
                



    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
        context ={

           
           'form' : form

        }
     
        return render(request, "start_1.html", context)


def homepage(request):
    
    print("Index Request Method :" , request.method )
    
    if request.method == "POST" :

        print('This is the index post')
        
        
        if 'utm_source' in request.GET and 'utm_medium' in request.GET and 'utm_campaign' in request.GET:
            
           
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            the_session = request.session.session_key

            data_entry = Log(utm_1=utm_source,utm_2=utm_medium,utm_3=utm_campaign,page='index',counter=1,session = the_session)
            data_entry.save()

            return redirect( f"{reverse('interstitial-page')}?{urlencode({'utm_source': utm_source })}&{urlencode({'utm_medium': utm_medium })}&{urlencode({'utm_campaign': utm_campaign })}")
        else :
            the_session = request.session.session_key
            data_entry = Log(utm_1='Unknown',utm_2='Unknown',utm_3='Unknown',page='index',counter=1,session = the_session)
            data_entry.save()
            

            return redirect('interstitial-page' ) 
    else :
        categories = Category.objects.all()[0:10]
        featured = Post.objects.order_by('-timestamp')[0:10]
        featured_other = Post.objects.filter(featured=True)[6:10]
        latest = Post.objects.order_by('-timestamp')[0:10]
        context= {
            'object_list': featured,
            'featured_other': featured_other,
            'latest': latest,
            'categories':categories,
                 
        }
        print("Thi is where")
        return render(request, 'index.html', context)


def interstitial(request):
    form = LoginForm(request.POST)
   
    if request.method == "POST":

        #return redirect('interstitial-page-1') 
        if 'utm_source' in request.GET and 'utm_medium' in request.GET and 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            the_session = request.session.session_key

            data_entry = Log(utm_1=utm_source,utm_2=utm_medium,utm_3=utm_campaign,page='interstitial',counter=1,session = the_session)
            data_entry.save()

            return redirect( f"{reverse('interstitial-page-1')}?{urlencode({'utm_source': utm_source })}&{urlencode({'utm_medium': utm_medium })}&{urlencode({'utm_campaign': utm_campaign })}")
        else :
            the_session = request.session.session_key
            data_entry = Log(utm_1='Unknown',utm_2='Unknown',utm_3='Unknown',page='interstitial',counter=1,session = the_session)
            data_entry.save()

            return redirect('interstitial-page-1' ) 
      
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

def interstitial_1(request):
    form = LoginForm(request.POST)
   
    if request.method == "POST":

           
        myurl = f'http://192.168.50.1/login.html'    
        
        #parameter_value_pairs = {"domain":domain,"hotspotname":domain_id}  
        #req_url = myurl +  urlencode(parameter_value_pairs)
        req_url = myurl
       
       
        
        return redirect(myurl)

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
        
        if 'utm_source' in request.GET and 'utm_medium' in request.GET and 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            the_session = request.session.session_key

            data_entry = Log(utm_1=utm_source,utm_2=utm_medium,utm_3=utm_campaign,page='interstitial_1',counter=1,session = the_session)
            data_entry.save()

        else :
            the_session = request.session.session_key
            data_entry = Log(utm_1='Unknown',utm_2='Unknown',utm_3='Unknown',page='interstitial_1',counter=1,session = the_session)
            data_entry.save()


        return render(request, 'interstitial_1.html', context)

  
def exit_page_1(request):
    form = LoginForm(request.POST)
   
    if request.method == "POST":
       
         return redirect('exit-page-2') 
       
    else :
        categories = Category.objects.all()[0:10]
        featured = Post.objects.filter(featured=True)[0:5]
        featured_other = Post.objects.filter(featured=True)[6:10]
        latest = Post.objects.order_by('-timestamp')[0:10]
        context= {
            'object_list': featured,
            'featured_other': featured_other,
            'latest': latest,
            'categories':categories,

        }
        
        return render(request, 'exit_page_1.html', context)

def exit_page_2(request):
    form = LoginForm(request.POST)
   
    if request.method == "POST":
       
       return redirect('exit-index') 
   
    else :
        categories = Category.objects.all()[0:10]
        featured = Post.objects.filter(featured=True)[0:5]
        featured_other = Post.objects.filter(featured=True)[6:10]
        latest = Post.objects.order_by('-timestamp')[0:10]
        context= {
            'object_list': featured,
            'featured_other': featured_other,
            'latest': latest,
            'categories':categories,

        }
        
        return render(request, 'exit_page_2.html', context)

def exit_index(request):
    form = LoginForm(request.POST)
    
    if request.method == "POST" :
        print('The is the INDEX post')
        return redirect('interstitial-page-nop') 
    else :
        categories = Category.objects.all()[0:10]
        featured = Post.objects.filter(featured=True)[0:5]
        featured_other = Post.objects.filter(featured=True)[6:10]
        latest = Post.objects.order_by('-timestamp')[0:10]
        context= {
            'object_list': featured,
            'featured_other': featured_other,
            'latest': latest,
            'categories':categories,
           
      
        }
        return render(request, "exit_index.html", context)


def post(request,slug):
    post = Post.objects.get(slug=slug)
    categories = Category.objects.all()[0:10]
    featured = Post.objects.filter(featured=True)[0:10]
    latest = Post.objects.order_by('-timestamp')[0:10]
    
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
         
    categories = Category.objects.all()[0:10]
    featured = Post.objects.filter(featured=True)[0:5]
    featured_other = Post.objects.filter(featured=True)[6:10]
    latest = Post.objects.order_by('-timestamp')[0:10]
    posts = Post.objects.order_by('-timestamp')
    context = {
        'posts': posts,
        'object_list': featured,
        'featured_other': featured_other,
        'latest': latest,
        'categories':categories,
      
    }
    return render(request, 'post_list.html', context)

