from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.db import IntegrityError
from django.utils.dateparse import parse_date

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
                return redirect('signout')
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
            'message': 'The form is missing values.'
        })
    
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            'success': True,
            'message': "You have successfully signed in!"
        })
    else:
        return JsonResponse({
            'success': False,
            'message': "You have provided an incorrect combination."
        })

@notAuthenticated
def authSignUp(request):
    if request.method != "POST": 
        return JsonResponse({
            'success': False,
            'message': 'Invalid action'
        })

    if 'username' not in request.POST or 'password' not in request.POST or 'email' not in request.POST or 'firstName' not in request.POST or 'lastName' not in request.POST or 'dateOfBirth' not in request.POST:
        return JsonResponse({ 'success': False, 'message': 'The form is incomplete!' })
    
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    first_name = request.POST['firstName']
    last_name = request.POST['lastName']
    date_of_birth = request.POST['dateOfBirth']

    existing_users = AppUser.objects.filter(username=username, email=email).count()
    if(existing_users > 0):
        return JsonResponse({
            'success': False,
            'message': "An account with these details is already registered!"
        })

    try: 
        dob = parse_date(date_of_birth)
    except ValueError:
        return JsonResponse({ 'success': False, 'message': 'You have specified an invalid Date of Birth.'})

    user = AppUser(username=username, first_name=first_name, last_name=last_name, email=email, date_of_birth=dob)
    user.set_password(password)
    try:
        user.save()
    except IntegrityError:
        return JsonResponse({ 'success': False, 'message': "An account with these details is already registered!" })

    login(request, user)
    return JsonResponse({ 'success': True, 'message': "Your account has been created." })


def authSignOut(request):
    # Let user logout regardless if they were logged in or not.
    logout(request)
    return redirect('auth')

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