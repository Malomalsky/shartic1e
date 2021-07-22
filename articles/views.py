from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Article, ShortDescription
from .scripts import is_string_an_url
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from .forms import NewShortForm, NewArticleForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from profiles.models import Profile

def index(request):
    return render(request, 'articles/index.html')


def last_articles(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, 'articles/article_list.html', context=context)


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    shorts = sorted(article.short.all(), key=lambda a: a.rating, reverse=True)
    form = NewShortForm()
    authors = set()
    for short in ShortDescription.objects.filter(author=request.user, article=article):
        authors.add(short.author)
    print(authors)
    context = {
        "article": article,
        "shorts": shorts,
        "form": form,
        "authors": authors
    }
    return render(request, 'articles/article_detail.html', context=context)


def search_article(request):
    if request.method == "GET":
        search_query = request.GET.get("q")
        if search_query:
            if is_string_an_url(search_query):
                try:
                    search_results = Article.objects.get(url=search_query)
                    return redirect(reverse('article_detail', kwargs={'article_id': search_results.id}))
                except ObjectDoesNotExist:
                    print('Нет такого')
            else:
                search_results = Article.objects.filter(header__search=search_query).distinct()
            if len(search_results) > 5:
                paginator = Paginator(search_results, 5)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                context = {
                    "page_obj": page_obj,
                    "q": request.GET.get('q')
                }
            else:
                context = {
                    "articles": search_results
                }
    return render(request, 'articles/article_list.html', context=context)


@login_required
def handle_opinion(request):

    if request.method == "POST":

        short_id = request.POST.get('short_id')
        opinion = request.POST.get('opinion')
        short_obj = get_object_or_404(ShortDescription, id=short_id)
        profile = Profile.objects.get(user=short_obj.author)

        if opinion == 'like':
            if short_obj.likes.filter(id=request.user.id):
                short_obj.likes.remove(request.user)
                profile.rating -= 1
                profile.save()
            else:
                if short_obj.dislikes.filter(id=request.user.id):
                    short_obj.dislikes.remove(request.user)
                short_obj.likes.add(request.user)
                profile.rating += 1
                profile.save()

        elif opinion == 'dislike':
            if short_obj.dislikes.filter(id=request.user.id):
                short_obj.dislikes.remove(request.user)
                profile.rating += 1
                profile.save()
            else:
                if short_obj.likes.filter(id=request.user.id):
                    short_obj.likes.remove(request.user)
                short_obj.dislikes.add(request.user)
                profile.rating -= 1
                profile.save()

        html = render_to_string(
            template_name='articles/short_description.html',
            context={"short": short_obj},
            request=request
        )
        return HttpResponse(html)


@login_required
def create_short(request, article_id):
    if request.method == "POST":
        article = get_object_or_404(Article, id=article_id)
        short_form = NewShortForm(request.POST)
        if short_form.is_valid():
            new_short = short_form.save(commit=False)
            new_short.article = article
            new_short.author = request.user
            new_short.save()
        return redirect(reverse('article_detail', kwargs={'article_id': article.id}))


@login_required
def add_new_article(request):
    if request.method == "GET":
        form = NewArticleForm()
        return render(request, 'articles/submit_article.html', {'form': form})

    elif request.method == 'POST':
        article_form = NewArticleForm(request.POST)

        if article_form.is_valid():
            new_article = article_form.save()
            return redirect(reverse('article_detail', kwargs={'article_id': new_article.id}))
        elif article_form.errors.as_data()['url'][0].code == 'unique':
            messages.info(request, 'Article with this URL already in database')
            article = Article.objects.get(url=request.POST.get('url'))
            return redirect(reverse('article_detail', kwargs={'article_id': article.id}))


def leaderboard(request):
    users = ShortDescription.objects
    print(users)
