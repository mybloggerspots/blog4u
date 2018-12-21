from django import forms
from models import Comments,Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import EmailValidator
from taggit.forms import *

# Customized loginform with bootstrap styling
class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=('username','password')

    def clean(self):
        cleaned_data=super(LoginForm,self).clean()
        input_user=cleaned_data['username']
        if is_username_exists(input_user)==False:
            raise forms.ValidationError

# Signup form with bootstrap styling
class SignUpForm(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your name','style':'font-family:Arial;font-size:16px;margin-bottom:15px;height:36px !important'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Pick a username','style':'font-family:Arial;font-size:16px;margin-bottom:15px;height:36px !important'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your surname','style':'font-family:Arial;font-size:16px;margin-bottom:15px;height:36px !important'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Create a password','style':'font-family:Arial;font-size:16px;height:36px !important;'}),help_text="Make sure it's more than 15 characters, or atleast 8 characters, including alphabets and numbers.")
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'you@example.com','style':'font-family:Arial;font-size:16px;margin-bottom:15px;height:36px !important'}))
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

    def clean(self):
        print 'signup form clean method start'
        cleaned_data=super(SignUpForm,self).clean()
        # Firstname Validation
        print "first name val start"
        input_fname=cleaned_data['first_name']
        if len(input_fname)<5 or input_fname.isalpha()==False:
            raise forms.ValidationError('Firstname should be in alphabets and of length minimum 5 characters ')
        # Lastname Validation
        print "last name val start"
        input_lname=cleaned_data['last_name']
        if input_lname.isalpha()==False:
            raise forms.ValidationError('Last name should not have digits')
        input_username=cleaned_data['username']
        if len(input_username)<8:
            raise forms.ValidationError("Username should be of length 8 characters")
        input_password=cleaned_data['password']
        if len(input_password)<8 or input_password.isalnum()==False:
            raise forms.ValidationError("Week password.. Enter an alphanumeric value")
        if input_username==input_password:
            raise forms.ValidationError('Username and Password should not be same ')
        input_email=cleaned_data['email']
        if is_email(input_email)==True:
            if is_email_exists(input_email)==True:
                raise forms.ValidationError('Email address already exists')
        else:
            raise forms.ValidationError('Invalid Email Domain..')
        print "signupform clan method end"
class SendEmailForm(forms.Form):
    # name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    to=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'to-person@example.com'}))
    comments=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':6,'cols':20,'placeholder':'Share your views here'}))

class CommentsForm(forms.ModelForm):
    # name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    body=forms.CharField(widget=forms.Textarea(attrs={'rows':'1','cols':'100','style':'width:85%;border:none; border-bottom:0.5px solid grey;box-shadow:none;border-radius:0px;margin-left:15px;background:transparent;outline:0;margin-top:0px;','placeholder':'Add a public comment'}))
    class Meta:
        model=Comments
        fields=['body']

class PostForm(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Pick a title'}))
    body=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    tags=TagField()
    class Meta:
        model=Post
        widgets={'category':forms.Select(attrs={'class':'bootstrap-select','class':'form-control'}),
                 'status':forms.Select(attrs={'class':'bootstrap-select','class':'form-control'})}
                 # 'tags':forms.CharField(attrs={'class':'form-control'})}
                 # 'author':forms.Select(attrs={'class':'bootstrap-select','class':'form-control'})}
        fields=['title','category','status','tags','body']

def is_email(value):
    mails=['gmail.com','yahoo.com','outlook.com','hotmail.com']
    if(value[len(value)-9:] not in mails and value[len(value)-11:] not in mails):
        return False
    else:
        return True
def is_email_exists(value):
    if User.objects.filter(email=value).exists():
        return True
    else:
        return False

def is_username_exists(string):
    try:
        username=User.objects.filter(username=string)
    except User.DoesNotExist:
        return False
    return True
