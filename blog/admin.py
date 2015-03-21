import watson

# Register your models here.
from django.contrib import admin
from blog.models import Blog, Category, Author

class BlogAdmin(watson.SearchAdmin):
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", "body",) 

class CategoryAdmin(watson.SearchAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title",) 

class AuthorAdmin (watson.SearchAdmin):
	search_fields = ("name",) 
	prepopulated_fields = {'slug_name': ('name',)}

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)