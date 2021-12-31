from django.urls import path
from . import views
from .views import SendRequest

urlpatterns = [

    path('signup',views.SignUp.as_view(), name="signup"),
    path('signin',views.UserLogin.as_view(), name="login"),
    path('logout',views.LogoutView.as_view(), name="logout"),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile'),
    path('profileview/<int:pk>', views.ProfileView.as_view(), name='profileview'),
    path('friends', views.ListFriends.as_view(), name='friends'),
    path('requests', views.ListRequests.as_view(), name='requests'),
    path('sendrequest/<int:id>', views.SendRequest.as_view(), name='sendrequest'),
    path('acceptrequest/<int:id>', views.AcceptRequest.as_view(), name='acceptrequest'),
    path('rejectrequest/<int:id>', views.RejectRequest.as_view(), name='rejectrequest'),
    path('friendslist/<int:id>', views.FriendList.as_view(), name="friendslist"),


]