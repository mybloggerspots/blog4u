# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Post,Comments

class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','publish','body','created','updated','status','category']
    prepopulated_fields={'slug':('title',)}
    search_fields=('title','body')
    list_filter=('status','author','created','publish','category')
    raw_id_fields=('author',)
    date_hierarchy=('publish')
    ordering=('status','publish')
admin.site.register(Post,PostAdmin)

class CommentsAdmin(admin.ModelAdmin):
    list_display=('name','email','body','created','updated','active')
    list_filter=('active','created','updated')
    search_fields=('name','email','body')
admin.site.register(Comments,CommentsAdmin)
