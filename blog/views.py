from django.shortcuts import render
from django.template import RequestContext
from django.core.paginator import Paginator, \
    InvalidPage, EmptyPage
from blog.models import Author
from taggit.models import Tag
from django.conf import settings
from blog.models import Blog, Category, Author
from django.shortcuts import render_to_response, get_object_or_404



def home(request):
    return render_to_response("home.html",
                              context_instance=RequestContext(request))


def index(request):
    post = Blog.objects.all().order_by ('-created')
    entries_per_page = getattr(settings, 'BLOG_NUMBER_OF_ENTRIES_PER_PAGE')

    paginator = Paginator(post, entries_per_page)

    try:
        page_number = int(request.GET.get("page", '1'))
    except ValueError:
        page_number = 1

    try:
        page = paginator.page(page_number)
        posts = page.object_list
    except (InvalidPage, EmptyPage):
        page= paginator.page(paginator.num_pages)
        posts = page.object_list

    return render_to_response('index.html', {
        'categories': Category.objects.all() [:4],
        'posts':posts,
        'page': page,
    })

def view_post(request, slug):
    
    tags = Tag.objects.all()   
    return render_to_response('view_post.html', {
        'post': get_object_or_404(Blog, slug=slug),
        'categories': Category.objects.all(),
        'tags': tags,
    })


def view_category(request, slug):

    category = get_object_or_404(Category, slug=slug)
    post = Blog.objects.filter(category=category)
    entries_per_page = getattr(settings, 'BLOG_NUMBER_OF_ENTRIES_PER_PAGE')

    paginator = Paginator(post, entries_per_page)

    try:
        page_number = int(request.GET.get("page", '1'))
    except ValueError:
        page_number = 1

    try:
        page = paginator.page(page_number)
        posts = page.object_list
    except (InvalidPage, EmptyPage):
        page= paginator.page(paginator.num_pages)
        posts = page.object_list

    return render_to_response('view_category.html', {
        'category': category,
        'posts': posts,
        'categories': Category.objects.all() [:4],
        'page':page,
    })


def show_author(request, slug_name):
    try:
        author = Author.objects.filter(slug_name=slug_name).all()[0:1].get()
    except Exception, e:
        raise Http404
    article_list = author.blog_set.all()
    try:
        page_number = int(request.GET.get('page', '1'))
    except:
        page_number = 1
    paginator = Paginator(article_list, 10)
    try:
        page = paginator.page(page_number)
        related_articles = page.object_list
    except:
        page = paginator.page(paginator.num_pages)
        related_articles = page.object_list
    
    other_authors = Author.objects.exclude(id=author.id).all()
    
    return render_to_response('author_page.html', 
        {
         'author': author,
         'page': page,
         'other_authors': other_authors,
         'related_articles': related_articles
        }
    )
    

def tag_details(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Blog.objects.filter(tags__in=[tag])
    tags = Tag.objects.all()
    # tagged_entries = Post.objects.filter(tags__in=[tag])
    d = {'posts': posts, 'tag': tag, 
         'post_two': Blog.objects.all(), 'tags': tags}
    return render(request, "tag_details.html", d)


