from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from .forms import SearchForm
from django.db.models import Q

from .models import Article, Category, TagPost

menu = [{'title': "О проекте", 'url_name': 'about'}
]

data = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }


def index(request):
    posts = Article.published.all().select_related('cat')

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'maincontent/index.html', context=data)


def about(request):
    return render(request, 'maincontent/about.html', context=data)


def all_tags(request):
    categories = Category.objects.all()

    category_tags = []

    for category in categories:
        articles = Article.objects.filter(cat=category, is_published=True)
        tags = TagPost.objects.filter(tags__in=articles).distinct()

        if tags.exists():
            category_tags.append({
                'category': category,
                'tags': tags
            })

    return render(request, 'maincontent/all_tags.html', {
        'show_tags': False,
        'category_tags': category_tags,
        'menu': menu
    })


def show_post(request, post_slug):
    post = get_object_or_404(Article, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'maincontent/post.html', data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Article.published.filter(cat_id=category.pk).select_related('cat')

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
        'category_name': category.name,
    }
    return render(request, 'maincontent/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Article.Status.PUBLISHED).select_related('cat')

    categories = set(post.cat for post in posts if post.cat)

    category_name = None
    if len(categories) == 1:
        category_name = list(categories)[0].name

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
        'category_name': category_name,
    }

    return render(request, 'maincontent/index.html', context=data)


def search_articles(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Article.published.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(content__icontains=query)
            ).select_related('cat')

    data = {
        'title': f'Результаты поиска: {query}' if query else 'Поиск',
        'menu': menu,
        'form': form,
        'query': query,
        'results': results,
        'cat_selected': None,
    }
    return render(request, 'maincontent/search.html', context=data)