from allauth.socialaccount.models import SocialLogin
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User

@receiver(user_signed_up)
def save_email(sender, sociallogin, **kwargs):
    user = sociallogin.user
    user.email = sociallogin.account.extra_data.get('email')
    user.save()
    
class Story(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=400,default="")
    url = models.URLField()
    description = models.TextField(default="")
    title_single = models.CharField(max_length=400,default="")
    source = models.CharField(max_length=100,default="")
    author = models.CharField(max_length=100,default="", null=True)
    bookmarked_by = models.ManyToManyField(User, related_name='bookmarked_stories', blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    story = models.ForeignKey(Story, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    liked_by = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    karma_points = models.IntegerField()
    