from django.db import models
from django.db.models import permalink
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
import watson



# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    short_introduction = models.CharField(max_length=1024, blank=True, default='')
    email = models.EmailField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/author/' + self.slug_name

    def save(self, force_insert=False, force_update=False):
        if Author.objects.filter(slug_name=self.slug_name).exclude(pk=self.id).count() != 0:
            raise Exception('Duplicate slug title !!!')
        return super(Author, self).save(force_insert=force_insert, force_update=force_update)



class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    authors = models.ManyToManyField(Author, blank=True, related_name='blog_set')
    author_name = models.CharField(max_length=256, blank=True, default='')
    tags = TaggableManager()
    body = RichTextField()
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('blog.Category')
    photo = models.ImageField (upload_to = 'media/', blank = True, null = True)

    def __unicode__(self):
        return '%s' % self.title
    def get_authors_link(self):
        link = ''
        if self.authors.count() > 1:
            for author in self.authors.all():
                link = link + '<span><a href="' + author.get_absolute_url() + '">' + author.name + '</a></span>'
        else:
            for author in self.authors.all():
                link = link + '<span><a href="' + author.get_absolute_url() + '">' + author.name + '</a></span>'  
        if not link:
            link = self.author_name
        if link:
            return '<p>' + link + '</p>'
            
        else:
            return link

    def get_authors(self):
        link = ''
        if self.authors.count() > 1:
            for author in self.authors.all():
                link = link + '<span><a href="' + author.get_absolute_url() + '">' + author.name + '</a></span>'
        else:
            for author in self.authors.all():
                link = link + '<span><a href="' + author.get_absolute_url() + '">' + author.name + '</a></span>'
        if not link:
            link = u'<span>%s</span>' % self.author_name
        return link

    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, { 'slug': self.slug })

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_category', None, { 'slug': self.slug })



watson.register(Blog)
watson.register(Author)