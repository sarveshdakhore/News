from django.urls import path, include
from home import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApiKeyViewSet

router = DefaultRouter()
router.register(r'apikeys', ApiKeyViewSet)


urlpatterns = [
    path('',views.home,name="home"),
    path('', include(router.urls)),
    path('home/',views.home,name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('read/', views.read, name="read"),
    path('bookmark', views.bookmark, name="bookmark"),
    path('add_comment', views.add_comment, name="add_comment"),
    path('add_api_key/', views.add_api_key, name='add_api_key'),
    path('delete_api_key/<int:key_id>/', views.delete_api_key, name='delete_api_key'),
    path('get_story/',views.top_stories,name="get_story"),
]
