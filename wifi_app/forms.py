from django import forms
from .models import Comment,GameUser

class LoginForm(forms.Form):
    domain = forms.CharField(max_length=100)
    domainId = forms.CharField(max_length=100)
    mac = forms.CharField(max_length=100)
    ip = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    link_login = forms.CharField(max_length=100)
    link_orig = forms.CharField(max_length=100)
    error = forms.CharField(max_length=100)
    trial = forms.CharField(max_length=100)
    chap_id = forms.CharField(max_length=100)
    chap_challenge = forms.CharField(max_length=100)
    link_login_only = forms.CharField(max_length=100)
    link_orig_esc = forms.CharField(max_length=100)
    mac_esc = forms.CharField(max_length=100)
    identity = forms.CharField(max_length=100)
    bytes_in_nice = forms.CharField(max_length=100)
    bytes_out_nice = forms.CharField(max_length=100)
    session_time_left = forms.CharField(max_length=100)
    uptime = forms.CharField(max_length=100)
    refresh_timeout = forms.CharField(max_length=100)
    link_status = forms.CharField(max_length=100)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','cell_number', 'body','notify')
        labels = {'notify': 'I want to be notified if someone responds to your comment ?', 'body' : 'Your Comment',  'name' : 'Name and Surname'}
        
   


    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter your name amd surname here'}
        self.fields['cell_number'].widget.attrs = {'placeholder': 'Enter your 10 digit cell number ...','maxlength': '10'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...','class':'form-control', 'rows':'5'}




class OptOutForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('notify',)
        labels = {'notify': 'To stop receiving notifications untick this box and submit'}
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(OptOutForm, self).__init__(*args, **kwargs)
       
        self.fields['notify'].widget.attrs = {'class':'form-control'}


class GameForm(forms.ModelForm):
    class Meta:
        model = GameUser
        fields = "__all__"
        exclude = ('timestamp', 'username',)

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'large-font'
