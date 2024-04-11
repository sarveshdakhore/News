from django.urls import path, include
from home import views

urlpatterns = [
    path('',views.home,name="home"),
    path('home/',views.home,name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('read/', views.read, name="read"),
    path('bookmark', views.bookmark, name="bookmark")
]
