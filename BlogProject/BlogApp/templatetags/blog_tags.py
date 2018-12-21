from django import template
from BlogApp.models import Post
from django.db.models import Count
register=template.Library()

@register.simple_tag
def total_post_count():
    return Post.objects.count()

@register.inclusion_tag('BlogApp/latest_posts.html')
def latest_posts(count=4):
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'new_posts':latest_posts}

@register.assignment_tag()
def get_most_commented_posts(count=3):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('total_comments')[:count]

# @register.filter(name='tagnames')
# def get_tag_names(tags):
#     tag_names=[]
#     for tag in tags:
#         tag_names.append(tag.name)
#     return tag_names
