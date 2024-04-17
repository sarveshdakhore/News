from allauth.socialaccount.models import SocialLogin
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    UserProfile.objects.create(user=user)
    user.email = request.account.extra_data.get('email')
    user.save()
    
class Story(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=400,default="")
    url = models.URLField()
    urlToImage = models.URLField(default="")
    description = models.TextField(default="")
    title_single = models.CharField(max_length=400,default="")
    source = models.CharField(max_length=100,default="")
    author = models.CharField(max_length=100,default="", null=True)
    content = models.TextField(default="")
    
    def __str__(self):
        return f"{self.title} - {self.author} - {self.source}"

class Bookmark(models.Model):
    story = models.ForeignKey(Story, related_name='bookmarks', on_delete=models.CASCADE)
    userId = models.IntegerField(null=False)
    
    def __str__(self):
        return f"{self.story} - {self.userId}"

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    story = models.ForeignKey(Story, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    liked_by = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    karma_points = models.IntegerField(default=0)
    requests_this_hour = models.IntegerField(default=0)
    last_request_hour = models.IntegerField(default=timezone.now().hour)
    def __str__(self):
        return f"{self.user.username}"
    
    
class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, unique=True, null=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.key}"