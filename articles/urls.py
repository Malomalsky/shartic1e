from django.urls import path
from .views import (
    index,
    last_articles,
    article_detail,
    search_article,
    handle_opinion,
    create_short,
    add_new_article,
    leaderboard
)

urlpatterns = [
    path('', index, name='index'),
    path('articles/', last_articles, name='articles'),
    path('articles/<int:article_id>', article_detail, name='article_detail'),
    path('articles/<int:article_id>/new', create_short, name='create_short'),
    path('articles/new/', add_new_article, name='add_new_article'),
    path('leaderboard', leaderboard, name='leaderboard'),
    path('search/', search_article, name='search'),
    path('vote/', handle_opinion, name='handle_opinion'),
]

