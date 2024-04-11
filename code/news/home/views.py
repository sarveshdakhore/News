from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from .news import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# News API
# 2e25cce3b0d0481aab616a68309b885c
# Create your views here.
def home(request):
    l = get_top_stories()
    return render(request,'home/home.html', {'articles': l["articles"]})

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


def add_comment(request):
    if request.method == 'POST' and request.user.is_authenticated:
        comment = request.POST.get('comment')
        title = request.POST.get('title')
        link = request.POST.get('link')
        article = Story.objects.get(title=title)
        user = request.user
        
        comment = Comment.objects.create(user=user, story=article, text=comment)
        
        print(comment.text)
        
        comments_list = []
        comments = Comment.objects.filter(story=article)
        for commentq in comments:
            comment_data = [commentq.text, commentq.user.username]
            comments_list.append(comment_data)
        return render(request,'home/read.html',{"link":link, "title":title, "comments":comments_list})
    return redirect('home')


def article_detail(request, article_id):
    article = get_object_or_404(Story, id=article_id)
    comments = Comment.objects.filter(article=article)
    return render(request, 'article_detail.html', {'article': article, 'comments': comments})

@csrf_exempt
def bookmark(request):
    if request.method == 'POST' and request.user.is_authenticated:
        print("\n\n\n\n\nlkolokojol")
        title = request.POST.get('title')
        story = Story.objects.get(title=title)
        print(story.title)
        user = request.user.id
        bookmark, created = Bookmark.objects.get_or_create(story=story, userId=user)
        if created:
            return JsonResponse({"status": "1"})  # Bookmark added
        else:
            bookmark.delete()
            return JsonResponse({"status": "0"})  # Bookmark removed
    return JsonResponse({"status": "4"})  # Invalid request or user not authenticated
    
