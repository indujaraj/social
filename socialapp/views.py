from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, ListView, DeleteView
from . import decorators
from django.utils.decorators import method_decorator

from posts.models import Post
from .decorators import signin_required
from .forms import RegisterForm, LoginForm, ProfileForm, ContactFormEmail

from .models import Profile, Relationship


class SignUp(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'SignUp.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            profile, created = Profile.objects.get_or_create(user=user)

        return redirect('/socialapp/signin')


class UserLogin(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {'form': form}
        return render(request, 'SignIn.html', context)

    def post(self, request):
        form = LoginForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/posts/timeline')
        else:
            return render(request, 'SignIn.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/socialapp/signin')


@method_decorator(signin_required, name="dispatch")
class ProfileDetailView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = '/posts/timeline'


@method_decorator(signin_required, name="dispatch")
class ProfileView(DetailView):
    model = Profile
    template_name = 'profileview.html'


@method_decorator(signin_required, name="dispatch")
class ListFriends(ListView):
    model = Profile
    template_name = 'friends.html'
    context_object_name = 'users'

    def get_queryset(self):
        return Profile.objects.exclude(user=self.request.user)


@method_decorator(signin_required, name="dispatch")
class SendRequest(View):
    def get(self, request, id, *args, **kwargs):
        sender = self.request.user.profile
        receiver = Profile.objects.get(id=id)
        friend_request, created = Relationship.objects.get_or_create(sender=sender, receiver=receiver, status='sent')
        messages.success(request, 'Request sent')

        return HttpResponse('friend request sent')

        return render(request, 'friends.html')


@method_decorator(signin_required, name="dispatch")
class ListRequests(ListView):
    model = Relationship
    template_name = 'requests.html'
    context_object_name = 'friend_requests'

    def get_queryset(self):
        return Relationship.objects.filter(receiver=self.request.user.profile)


@method_decorator(signin_required, name="dispatch")
class AcceptRequest(View):
    def get(self, request, id, *args, **kwargs):
        friend_request = Relationship.objects.get(id=id)
        friend_request.sender.user.friends.add(friend_request.receiver)
        friend_request.receiver.user.friends.add(friend_request.sender)
        if friend_request.status == 'sent':
            friend_request.status = 'accepted'

            return HttpResponse('friend request accepted')
        messages.success(request, 'Request accepted')

        return render(request, 'requests.html')


@method_decorator(signin_required, name="dispatch")
class RejectRequest(View):
    def get(self, request, id, *args, **kwargs):
        friend_request = Relationship.objects.get(id=id)
        if friend_request.status == 'sent':
            friend_request.status = 'rejected'

            return HttpResponse('friend request rejected')
        messages.error(request, 'Request rejected')
        return render(request, 'requests.html')


@method_decorator(signin_required, name="dispatch")
class FriendList(ListView):
    model = Profile

    def get(self, request, id, *args, **kwargs):
        profile = Profile.objects.get(id=id)
        friends = profile.friends.all()
        context = {
            'friends': friends
        }

        return render(request, 'friendslist.html', context)


@method_decorator(signin_required, name="dispatch")
class DeleteProfile(DeleteView):
    model = User
    pk_url_kwarg = 'id'
    template_name = 'deleteprofile.html'
    success_url = "/socialapp/signin"



def contactsendmail(request):
    if request.method == 'GET':
        form = ContactFormEmail()

    else:
        form = ContactFormEmail(request.POST)
        if form.is_valid():
            fromemail = form.cleaned_data['fromemail']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, fromemail, ['dobblesocial@gmail.com', fromemail])
    return render(request, 'contactpage.html', {'form': form})
