# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404,render_to_response
from models import Post,Comments
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.mail import send_mail
from forms import SendEmailForm,CommentsForm,SignUpForm,LoginForm,PostForm
from taggit.models import Tag
from django.contrib.auth.models import User
from . import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from django.template import RequestContext
from django.views.generic import UpdateView

def signup(request,form):
    user=None
    if form.is_valid():
        first_name=form.cleaned_data['first_name']
        last_name=form.cleaned_data['last_name']
        username=form.cleaned_data['username']
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
        user=form.save()
        user.first_name=first_name.title()
        user.last_name=last_name.title()
        print user
        user.set_password(user.password)
        return user

def index_view(request):
    if request.method=='POST':
        form=forms.SignUpForm(request.POST)
        user=signup(request,form)
        if user:
            user.save()
            login(request,user)
            return HttpResponseRedirect('/home')
    else:
        form=forms.SignUpForm()
    return render(request,'BlogApp/index.html',{'form':form})

def signup_view(request):
    if request.method=='POST':
        form=forms.SignUpForm(request.POST)
        user=signup(request,form)
        if user:
            user.save()
            login(request,user)
            return HttpResponseRedirect('/home')
    else:
        form=forms.SignUpForm()
    return render(request,'BlogApp/signup.html',{'form':form})

def post_list_view(request,tag_slug=None):
    user=request.user
    tag=None
    manage_posts=None
    posts_by_author=None
    postcount=Post.objects.filter(author=request.user.id).count()
    post_list=Post.objects.all()
    if not tag_slug:
        catgs=Post.objects.values('category')
        post_catgs=[]
        for i in catgs:
            for k,v in i.items():
                if v not in post_catgs:
                    post_catgs.append(v)
        from urlparse import urlparse
        post_uri=request.build_absolute_uri()
        parse_object = urlparse(post_uri)
        path=parse_object.path.split('/')
        if 'userposts' in path:
            post_list=Post.objects.filter(author=request.user.id)
            posts_by_author=True
        else:
            for ccat in post_catgs:
                for pcat in path:
                    if ccat==pcat:
                        if (pcat!='home')or(pcat!='othernews'):
                            post_list=Post.objects.filter(category=pcat)

    elif tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,5)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=Paginator.page(paginator.num_pages)

    return render(request,'BlogApp/post_list.html',{'post_list':post_list,'tag':tag,'posts_by_author':posts_by_author,'postcount':postcount,'manage_posts':manage_posts})

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',
                                                    publish__year=year,
                                                    publish__month=month,
                                                    publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    e_form=None
    email=None
    name=None
    logged_user=None
    user=request.user
    if request.user.is_authenticated():
        logged_user=request.user.username
        name=request.user.first_name
        email=request.user.email
    if request.method=='POST':
        form=CommentsForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.name=logged_user
            new_comment.email=email
            new_comment.post=post
            new_comment.save()
            csubmit=True
            e_form=CommentsForm()
    else:
        form=CommentsForm()
    return render(request,'BlogApp/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments,'e_form':e_form,'logged_user':logged_user,'name':name})

def sent_email_form_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    email=None
    name=None
    first_name=None
    user=request.user
    if request.user.is_authenticated():
        name=request.user.username
        email=request.user.email
        first_name=request.user.first_name
    if request.method=='POST':
        form=SendEmailForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) recommends you to read "{}"'.format(first_name.title(),email,post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message="Read the post at \n {} n\n {}\'s Comments: \n{}".format(post_url,first_name.title(),cd['comments'])
            send_mail(subject,message,'Blogger@blog.com',[cd['to']])
            sent=True
    else:
        form=SendEmailForm()
    return render(request,'BlogApp/email_share.html',{'form':form,'post':post,'sent':sent})

def logout_view(request):
    request.user=None
    return HttpResponseRedirect('/indexsignup')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/home')
    else:
        form =LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def post_view(request,id=None):
    post_sent=None
    post_title=None
    post_update=None
    post=None
    user_name=request.user.username
    form=PostForm()
    if id:
        post=get_object_or_404(Post,id=id)
        form=forms.PostForm(instance=post)
        post_update=True
    if request.method=='POST':
        form=forms.PostForm(request.POST,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            tags=form.cleaned_data['tags']
            post.author=request.user
            post.save()
            for tag in tags:
                post.tags.add(tag)
            post_title=post.title
            post_sent=True

    return render(request,'BlogApp/post_form.html',{'form':form,'post_sent':post_sent,'post_title':post_title,'post_update':post_update})

def post_object_view(request,id=None):
    post=get_object_or_404(Post,id=id)
    return render(request,'BlogApp/remove_post.html',{'post':post})

def post_delete_view(request,id=None):
    post_delete=None
    if id:
        post=get_object_or_404(Post,id=id)
        post.delete()
        post_delete=True
    return render(request,'BlogApp/remove_post.html',{'post':post,'post_delete':post_delete})

# class PostFormView(UpdateView):
#     model=Post
#     form_class=PostForm
#     pk_url_kwarg='id'
#     success_url='/userposts'
