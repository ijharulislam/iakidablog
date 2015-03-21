import os
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import *



urlpatterns = patterns('',
    # Examples:

   url(r'^$', 'blog.views.home', name='home'),
	   (r'^blog$', 'blog.views.index'),
   url(
		r'^blog/view/(?P<slug>[^\.]+).html', 
		'blog.views.view_post', 
		name='view_blog_post'),

    url(r'^blog/category/(?P<slug>[^\.]+).html', 
		'blog.views.view_category', 
		name='view_blog_category'),

	url(
		r'^author/(?P<slug_name>[\w\-]+)$', 
		'blog.views.show_author',),

	url(r"^blog/tag/(?P<tag_slug>[-\w]+)/$",
	  'blog.views.tag_details',
        name='tag_details'),


	url(r'^media/(?P<path>.*)$', 
		'django.views.static.serve', 
		{'document_root': os.path.join(os.path.dirname (__file__), 'media') }),

    url(r"^search/", include("watson.urls", namespace="watson")),
  
    (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

