from django.shortcuts import render, redirect
from .models import Article
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms


def article_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request, 'blog/article_list.html', { 'articles': articles })

def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    return render(request, 'blog/article_detail.html', { 'article': article })


@login_required()
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, 'blog/article_create.html', { 'form': form })