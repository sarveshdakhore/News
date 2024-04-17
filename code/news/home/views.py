from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from .news import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import ApiKeySerializer
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from functools import wraps
from django.http import HttpResponse
from django.db import IntegrityError



from functools import wraps
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import ApiKey, UserProfile

def api_key_and_rate_limit_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check API key
        api_key = request.META.get('HTTP_API_KEY')  # Adjust to use 'HTTP_API_KEY'
        print("\n\n\n\n\n\n")
        print(request.META)
        print(request.META.get('HTTP_API_KEY'))
        if not api_key:
            return JsonResponse({'error': 'API key is missing'}, status=401)
        
        api_key_obj = ApiKey.objects.filter(key=api_key).first()
        if not api_key_obj:
            return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        # Check rate limit
        user = api_key_obj.user
        user_profile = UserProfile.objects.get(user=user)
        current_hour = timezone.now().hour

        if user_profile.last_request_hour != current_hour:
            user_profile.requests_this_hour = 0
            user_profile.last_request_hour = current_hour

        user_profile.requests_this_hour += 1
        user_profile.save()

        if user_profile.requests_this_hour > 100:
            return HttpResponse('Rate limit exceeded', status=429)

        return view_func(request, user, *args, **kwargs)
    
    return _wrapped_view

@csrf_exempt
@api_key_and_rate_limit_required
def add_comment(request, user):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        title = request.POST.get('title')
        link = request.POST.get('link')
        article = Story.objects.get(title=title)
        comment = Comment.objects.create(user=user, story=article, text=comment_text)
        comments_list = []
        comments = Comment.objects.filter(story=article)
        for commentq in comments:
            comment_data = {'text': commentq.text, 'username': commentq.user.username}
            comments_list.append(comment_data)
        return JsonResponse({"link": link, "title": title, "comments": comments_list})
    return JsonResponse({'status': 'Invalid request method'}, status=405)


@csrf_exempt
@api_key_and_rate_limit_required
def bookmark(request, user):
    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST.get('title')
        story = Story.objects.get(title=title)
        bookmark, created = Bookmark.objects.get_or_create(story=story, userId=user.id)
        if created:
            return JsonResponse({"status": "1"})  # Bookmark added
        else:
            bookmark.delete()
            return JsonResponse({"status": "0"})  # Bookmark removed
    return JsonResponse({"status": "4"})  # Invalid request or user not authenticated


def home(request):
    if request.user.is_authenticated:
        api_keys = ApiKey.objects.filter(user=request.user)
    else:
        api_keys = None
    return render(request,'home/home.html', {'api_keys': api_keys})

def logout_view(request):
    logout(request)
    return redirect('home')

def read(request):
    link = request.POST.get('url')
    title = request.POST.get('title')
    article = Story.objects.get(title=title)
    comments_list = []
    comments = Comment.objects.filter(story=article)
    for comment in comments:
        comment_data = [comment.text, comment.user.username]
        comments_list.append(comment_data)
    return render(request,'home/read.html',{"link":link, "title":title, "comments":comments_list})

@csrf_exempt
@api_key_and_rate_limit_required
def top_stories(request, user):
    l = get_top_stories()
    return JsonResponse({'articles': l["articles"]})


import uuid


@login_required
def delete_api_key(request, key_id):
    if request.method == 'POST':
        api_key = ApiKey.objects.get(id=key_id, user=request.user)
        api_key.delete()
    return redirect('home')


@login_required
def add_api_key(request):
    if request.method == 'POST':
        while True:
            api_key = str(uuid.uuid4())
            try:
                ApiKey.objects.create(user=request.user, key=api_key)
                break
            except IntegrityError:
                continue
    return redirect('home')

class ApiKeyViewSet(viewsets.ModelViewSet):
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.apikey_set.all()

class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_API_KEY')
        if not api_key:
            return None

        try:
            api_key_obj = ApiKey.objects.get(key=api_key)
        except ApiKey.DoesNotExist:
            raise AuthenticationFailed('No such API Key')

        return (api_key_obj.user, None)
    

