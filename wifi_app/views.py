from urllib import request
from django.views.generic import TemplateView, ListView, DetailView, CreateView , UpdateView,FormView,DeleteView,View
from django.shortcuts import render,redirect, reverse,get_object_or_404
from django.urls import NoReverseMatch, reverse_lazy
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseRedirect
from .forms import LoginForm,CommentForm,OptOutForm
from .models import *
from data.models import *
from django.utils.http import urlencode
from getmac import get_mac_address as gma
from uuid import uuid4
from vouchers.forms import ActivationForm
from vouchers.mixins import OrganisorAndLoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


# Create your views here.



def test(request):
    posts = Post.objects.all()
    
    context = {
        'post': posts,
       
    }
    t = request.GET.get('Test') # => [137]
   
    myurl = "http://192.168.50.1/flash/hotspot/login2.html" 
    
 

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

            categories = Category.objects.all()[0:10]
            featured = Post.objects.filter(featured=True)[0:5]
            featured_other = Post.objects.filter(featured=True)[6:10]
            latest = Post.objects.order_by('-timestamp')[0:10]
            topics = Topic.objects.all().latest('pk')
            the_id = Topic.objects.values_list('pk', flat=True).latest('pk')
            comments = Comment.objects.filter(topic = the_id).order_by('-pk')[0:4]
            context= {
                'object_list': featured,
                'featured_other': featured_other,
                'latest': latest,
                'categories':categories,
                'topics':topics,
                'comments':comments,
            
        
            }
            return render(request, "exit_index.html", context)
             

def landing_page(request):

           
    if request.method == "POST" :
        # create a form instance and populate it with data from the request:
        the_session = str(uuid4())
        if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            redirect_destination = f"{reverse('landing-page-1')}?{urlencode({'utm_source': utm_source })}&{urlencode({'utm_medium': utm_medium })}&{urlencode({'utm_campaign': utm_campaign })}&{urlencode({'sid': the_session })}"
        else :
            redirect_destination = f"{reverse('landing-page-1')}?{urlencode({'sid': the_session })}"

        try :
            
            if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
                return redirect(redirect_destination)
            else :
                return redirect(redirect_destination)
        
        except Exception:

            pass

        finally : 

            if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
                data_entry = Log(utm_1=utm_source,utm_2=utm_medium,utm_3=utm_campaign,page='landing',counter=1,session = the_session )
                data_entry.save()
                               
            else :
                data_entry = Log(utm_1='Unknown',utm_2='Unknown',utm_3='Unknown',page='landing',counter=1,session = the_session)
                data_entry.save()

    else:

             
        try :
            return render(request, "start.html")
          
        except Exception:
                
            pass


       

def landing_page_1(request):
           
    if request.method == "POST" :

        the_session =  request.GET['sid']

        if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            redirect_destination = f"{reverse('home-page')}?{urlencode({'utm_source': utm_source })}&{urlencode({'utm_medium': utm_medium })}&{urlencode({'utm_campaign': utm_campaign })}&{urlencode({'sid': the_session })}"
        else :
            redirect_destination = f"{reverse('home-page')}?{urlencode({'sid': the_session })}"

        
        try :
        
            if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
                    return redirect( redirect_destination)
            else :
                return redirect(redirect_destination)  
                
        except Exception:

            pass

        finally : 

            if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
                data_entry = Log(utm_1=utm_source,utm_2=utm_medium,utm_3=utm_campaign,page='landing_1',counter=1,session = the_session )
                data_entry.save()
                               
            else :
               
                data_entry = Log(utm_1='Unknown',utm_2='Unknown',utm_3='Unknown',page='landing_1',counter=1,session = the_session)
                data_entry.save()


    # if a GET (or any other method) we'll create a blank form
    else:

        
        try :
            return render(request, "start_1.html")
          
        except Exception:
                
            pass

       

def homepage(request):
    
   
    
    if request.method == "POST" :
        the_session =  request.GET['sid']

        if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            redirect_destination = f"{reverse('interstitial-page')}?{urlencode({'utm_source': utm_source })}&{urlencode({'utm_medium': utm_medium })}&{urlencode({'utm_campaign': utm_campaign })}&{urlencode({'sid': the_session })}"
        else :
            redirect_destination = f"{reverse('interstitial-page')}?{urlencode({'sid': the_session })}"
        
        try :
        
   
            if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
                return redirect(redirect_destination)
            else :
            
                return redirect(redirect_destination)  
   
        except Exception:

            pass

        finally : 

            if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
                data_entry = Log(utm_1=utm_source,utm_2=utm_medium,utm_3=utm_campaign,page='home',counter=1,session = the_session )
                data_entry.save()
                               
            else :
               
                data_entry = Log(utm_1='Unknown',utm_2='Unknown',utm_3='Unknown',page='home',counter=1,session = the_session)
                data_entry.save()
   
   
   
   
    else :
      
        categories = Category.objects.all()[4:10]
        featured = Post.objects.order_by('-timestamp')[3:11]
        featured_other = Post.objects.filter(featured=True)[6:11]
        latest = Post.objects.order_by('-timestamp')[4:11]
        topics = Topic.objects.all().latest('pk')
        the_id = Topic.objects.values_list('pk', flat=True).latest('pk')
        comments = Comment.objects.filter(topic = the_id).order_by('-pk')[0:4]
       
        context= {
                'object_list': featured,
                'featured_other': featured_other,
                'latest': latest,
                'categories':categories,
                'topics':topics,
                'comments':comments,
            
        
            }
       
        try :

            categories = Category.objects.all()[0:10]
            featured = Post.objects.filter(featured=True)[0:5]
            featured_other = Post.objects.filter(featured=True)[6:10]
            latest = Post.objects.order_by('-timestamp')[0:10]
            topics = Topic.objects.all().latest('pk')
            the_id = Topic.objects.values_list('pk', flat=True).latest('pk')
            comments = Comment.objects.filter(topic = the_id).order_by('-pk')[0:4]
            context= {
                'object_list': featured,
                'featured_other': featured_other,
                'latest': latest,
                'categories':categories,
                'topics':topics,
                'comments':comments,
            
        
            }

            return render(request, 'index.html', context)
          
        except Exception:
                
            pass
      
        


def interstitial(request):
    form = LoginForm(request.POST)
   
    if request.method == "POST":

        the_session =  request.GET['sid']

        if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            redirect_destination = f"{reverse('interstitial-page-1')}?{urlencode({'utm_source': utm_source })}&{urlencode({'utm_medium': utm_medium })}&{urlencode({'utm_campaign': utm_campaign })}&{urlencode({'sid': the_session })}"
        else :
            redirect_destination = f"{reverse('interstitial-page-1')}?{urlencode({'sid': the_session })}"
        
        
        try :

            if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
               
                return redirect(redirect_destination)
            else :
               
                return redirect(redirect_destination) 

        except Exception:

            pass

        finally : 

            if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
                data_entry = Log(utm_1=utm_source,utm_2=utm_medium,utm_3=utm_campaign,page='interstitial',counter=1,session = the_session )
                data_entry.save()
                               
            else :
               
                data_entry = Log(utm_1='Unknown',utm_2='Unknown',utm_3='Unknown',page='interstitial',counter=1,session = the_session)
                data_entry.save() 
      
    else :
       
        try :
            return render(request, 'interstitial.html')
          
        except Exception:
                
            pass

       
        
def interstitial_1(request):
    form = LoginForm(request.POST)
   
    if request.method == "POST":

        the_session =  request.GET['sid']

        if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            redirect_destination  = f'http://192.168.50.1/login.html' 
        else :
            redirect_destination  = f'http://192.168.50.1/login.html' 
            

        try :

            return redirect(redirect_destination)

        except Exception:

            pass

                       
    else :
        

        try :
            return render(request, 'interstitial_1.html')
          
        except Exception:
                
            pass

            
          
def exit_page_1(request):
    form = LoginForm(request.POST)
   
    if request.method == "POST":

        the_session =  request.GET['sid']

        if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
            utm_source = request.GET['utm_source']
            utm_medium = request.GET['utm_medium']
            utm_campaign = request.GET['utm_campaign']
            redirect_destination = f"{reverse('exit-page-1')}?{urlencode({'utm_source': utm_source })}&{urlencode({'utm_medium': utm_medium })}&{urlencode({'utm_campaign': utm_campaign })}&{urlencode({'sid': the_session })}"
        else :
            redirect_destination = f"{reverse('exit-page-1')}?{urlencode({'sid': the_session })}"
        
        
        try :

            if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
               
                return redirect(redirect_destination)
            else :
               
                return redirect(redirect_destination) 

        except Exception:

            pass

        finally : 

            if 'utm_source' in request.GET or 'utm_medium' in request.GET or 'utm_campaign' in request.GET:
                data_entry = Log(utm_1=utm_source,utm_2=utm_medium,utm_3=utm_campaign,page='exit_1',counter=1,session = the_session )
                data_entry.save()
                               
            else :
               
                data_entry = Log(utm_1='Unknown',utm_2='Unknown',utm_3='Unknown',page='1xit_1',counter=1,session = the_session)
                data_entry.save() 
      
    else :
       
        try :
            return render(request, 'exit_page_1.html')
          
        except Exception:
                
            pass

       

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
       
        return redirect('interstitial-page-nop') 
    else :
        categories = Category.objects.all()[0:10]
        featured = Post.objects.filter(featured=True)[0:5]
        featured_other = Post.objects.filter(featured=True)[6:10]
        latest = Post.objects.order_by('-timestamp')[0:10]
        topics = Topic.objects.all().latest('pk')
        the_id = Topic.objects.values_list('pk', flat=True).latest('pk')
        comments = Comment.objects.filter(topic = the_id).order_by('-pk')[0:4]
        context= {
            'object_list': featured,
            'featured_other': featured_other,
            'latest': latest,
            'categories':categories,
            'topics':topics,
            'comments':comments,
           
      
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

class ActivationView(SuccessMessageMixin,OrganisorAndLoginRequiredMixin,CreateView):
    template_name = 'activation.html'
    form_class = ActivationForm
    success_message = "%(voucher_type)s voucher issued to %(cell_number)s  successfully"
    success_url = reverse_lazy('activation')
    
def topic_list(request):
         
    topics = Topic.objects.all()

    context = {
        'topics': topics,
      
    }
    return render(request, 'topic_list.html', context)

def topic_detail(request, slug):
    topic=get_object_or_404(Topic,slug=slug)
    #topic = Topic.objects.get(slug=slug)
    # List of active comments for this post
    comments = topic.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm(data=request.POST)
    
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.topic = topic
            # Save the comment to the database
            new_comment.save()
            # redirect to same page and focus on that comment
            return redirect(topic.get_absolute_url()+'#'+str(new_comment.id))
        else:
            comment_form = CommentForm()
            
            

    return render(request, 'topic_detail.html',{'topic':topic,'comments': comments,'comment_form':comment_form})

# handling reply, reply view
def reply_page(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            topic_id = request.POST.get('topic_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            topic_url = request.POST.get('topic_url')  # from hidden input
            reply = form.save(commit=False)
    
            reply.topic = Topic(id=topic_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(topic_url+'#'+str(reply.id))
    return redirect("/")


def comment_detail_optout(request, pk):
  
    
    the_comment = Comment.objects.get(id=pk)
    
    if request.method == 'POST':
        # A comment was posted
        form = OptOutForm(request.POST,instance=the_comment)
        if form.is_valid():
            form.save()
          
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
            #return render(request, "exit_index.html", context)
            return redirect('exit-index')
    else:
        form = OptOutForm(instance=the_comment)


    return render(request, 'comment_detail_oo.html',{'comment':the_comment, 'form':form})
