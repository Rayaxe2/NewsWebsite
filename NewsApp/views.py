from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from NewsApp.models import AppUser, NewsArticle, NewsCategory

def authenticated(view):
    # Decorator that protects view from unregistered users.
    def auth_check(request):
        if request.user.is_authenticated:
            username = request.user.username
            try:
                user = AppUser.objects.get(username=username)
            except AppUser.DoesNotExist:
                # Log user out if not existing within system.
                return logout(request)
            return view(request, user)
        else:
            return redirect('auth')
    return auth_check

def notAuthenticated(view):
    # Decorator that protects view from registered users.
    def not_auth_check(request):
        if request.user.is_authenticated:
            username = request.user.username
            try:
                user = AppUser.objects.get(username=username)
            except AppUser.DoesNotExist:
                return redirect('index')
            return redirect('index')
        else:
            return view(request)
    return not_auth_check

@notAuthenticated
def authForm(request):
    return render(request, 'NewsApp/authentication.html', {
        'title': 'Authentication'
    })

@notAuthenticated
def authSignIn(request):
    if request.method != "POST": 
        return JsonResponse({
            'success': False,
            'message': 'Invalid action'
        })

    if 'username' not in request.POST or 'password' not in request.POST:
        return JsonResponse({
            'success': False,
            'message': 'Incomplete form'
        })
    
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            'success': True
        })
    else:
        return JsonResponse({
            'success': False,
            'message': "You have provided an incorrect combination."
        })

@authenticated
def news(request, user):
    categories = NewsCategory.objects.all().annotate(
        article_count = Count('articles')
    )

    articles = NewsArticle.objects.all().annotate(
        like_count = Count('likes')
    )
    return render(request, 'NewsApp/index.html', {
        'title': 'News',
        'categories': categories,
        'articles': articles
    })