from django.urls import path

from . import views
# from .views import PostListView, MyPosts, AddLike, AddDislike,
from posts import views

urlpatterns = [
    path('timeline', views.PostListView.as_view(), name="timeline"),
    path('post/<int:pk>/like',views.AddLike.as_view(), name='like'),

    path('post/<int:pk>/dislike',views.AddDislike.as_view(), name='dislike'),
    path('myposts',views.MyPosts.as_view(), name="myposts"),
    path('post/like/<int:pk>',views.AddRestLike.as_view())


]
