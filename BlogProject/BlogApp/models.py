from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase

# class GenericStringTaggedItem(CommonGenericTaggedItemBase, TaggedItemBase):
#     object_id = models.CharField(max_length=50, verbose_name=('Object id'), db_index=True)

class TaggedPost(TaggedItemBase):
    content_object = models.ForeignKey('Post')

class PostModelManager(models.Manager):
    def get_queryset(self):
        return super(PostModelManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    title=models.CharField(max_length=256)
    CATEGORY_CHOICES=(('politics','Politics'),('business','Business'),('sports','Sports'),('films','Films'),('technology','Technology'))
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    slug=models.SlugField(max_length=256,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts')
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects=PostModelManager()
    tags=TaggableManager()
    category=models.CharField(max_length=20,choices=CATEGORY_CHOICES,default=None)
    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),
        self.publish.strftime('%d'),self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class Comments(models.Model):
    post=models.ForeignKey(Post,related_name='comments')
    name=models.CharField(max_length=256)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=('created',)
    def __str__(self):
        return 'Commented by {} on {} post'.format(self.name,self.post)
