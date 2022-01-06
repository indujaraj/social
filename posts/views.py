from django.contrib.auth.models import User
from django.core.serializers import json
from django.db.models import Q
from django.http import request, HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, FormView, DetailView, TemplateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator

from socialapp.decorators import signin_required
from socialapp.models import Profile
from .models import Post, Comment, ThreadModel, MessageModel
from .forms import PostForm, CommentForm, ThreadForm, MessageForm

# rest imports
from rest_framework.views import APIView
from rest_framework.response import Response


@method_decorator(signin_required, name="dispatch")
class PostListView(TemplateView):
    model = Post

    def get(self, request, *args, **kwargs):
        friends_list = list(self.request.user.profile.friends.all().values_list("profile__id", flat=True))

        posts = Post.objects.filter(author_id__in=friends_list)

        form = PostForm()
        context = {
            'posts': posts,
            'form': form
        }
        return render(request, 'timeline.html', context)

    def post(self, request, *args, **kwargs):
        friends_list = list(self.request.user.profile.friends.all().values_list("profile__id", flat=True))
        posts = Post.objects.filter(author_id__in=friends_list)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user.profile
            new_post.save()

        context = {
            'posts': posts,
            'form': form,
        }
        return redirect('/posts/myposts')
        return render(request, 'timeline.html', context)


@method_decorator(signin_required, name="dispatch")
class MyPosts(ListView):
    model = Post

    template_name = 'postdetail.html'
    context_object_name = 'my_posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user.profile)


@method_decorator(signin_required, name="dispatch")
class AddLike(View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user.profile:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user.profile)

        is_like = False

        for like in post.likes.all():
            if like == request.user.profile:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user.profile)

        if is_like:
            post.likes.remove(request.user.profile)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


@method_decorator(signin_required, name="dispatch")
class AddDislike(View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user.profile:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user.profile)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user.profile:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user.profile)

        if is_dislike:
            post.dislikes.remove(request.user.profile)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


@method_decorator(signin_required, name="dispatch")
class Comments(CreateView):
    model = Comment

    def post(self, request, *args, **kwargs):
        comment = request.POST.get("comment")
        pid = kwargs.get("id")
        comments = self.model(user=self.request.user.profile,
                              post_id=pid,
                              comment=comment
                              )
        comments.save()

        return redirect("timeline")


@method_decorator(signin_required, name="dispatch")
class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        context = {
            'form': form
        }
        return render(request, 'create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')
        receiver = User.objects.get(username=username)
        if ThreadModel.objects.filter(user=request.user.profile, receiver=receiver.profile).exists():
            thread = ThreadModel.objects.filter(user=request.user.profile, receiver=receiver.profile)[0]
            return redirect('thread', pk=thread.pk)
        elif ThreadModel.objects.filter(user=request.user.profile, receiver=receiver.profile).exists():
            thread = ThreadModel.objects.filter(user=request.user.profile, receiver=receiver.profile)[0]
            return redirect('thread', pk=thread.pk)

        if form.is_valid():
            sender_thread = ThreadModel(
                user=request.user.profile,
                receiver=receiver.profile
            )
            sender_thread.save()
            thread_pk = sender_thread.pk
            return redirect('thread', pk=thread_pk)

        else:
            return redirect('create-thread')


@method_decorator(signin_required, name="dispatch")
class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user.profile) | Q(receiver=request.user.profile))
        context = {
            'threads': threads
        }
        return render(request, 'inbox.html', context)


@method_decorator(signin_required, name="dispatch")
class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
            message = MessageModel(
                thread=thread,
                sender_user=request.user.profile,
                receiver_user=receiver,
                body=request.POST.get('message'),



            )
            message.save()
            return redirect('thread', pk=pk)
        return render(request, 'thread.html')


@method_decorator(signin_required, name="dispatch")
class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }
        return render(request, 'thread.html', context)


@method_decorator(signin_required, name="dispatch")
class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = Profile.objects.filter(
            Q(user__username__icontains=query)
        )

        context = {
            'profile_list': profile_list
        }

        return render(request, 'search.html', context)


@method_decorator(signin_required, name="dispatch")
class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'updatepost.html'
    success_url = '/posts/myposts'
    pk_url_kwarg = 'id'


@method_decorator(signin_required, name="dispatch")
class PostDelete(DeleteView):
    model = Post
    pk_url_kwarg = 'id'
    template_name = 'deletepost.html'
    success_url = "/posts/myposts"
