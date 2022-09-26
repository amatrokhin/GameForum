import re

import requests
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

from .models import Post, Reply
from .forms import PostsForm, ReplyForm
from .filters import PostsSelfFilter, ReplySelfFilter, ReplyOtherFilter


class PostsList(ListView):                      # list of all posts on site
    queryset = Post.objects.all().order_by('-time_in')
    template_name = 'posts_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):                   # responsible for detailed post output on a page
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(post__pk=self.kwargs['pk']).order_by('-time_in')
        return context


class PostCreate(LoginRequiredMixin, CreateView):      # responsible for creating news
    form_class = PostsForm
    model = Post
    template_name = 'post_edit.html'

    # set creator as author
    def form_valid(self, form):
        post = form.save(commit=False)

        # take author instance corresponding to the current user
        author = self.request.user

        form.instance.author = author
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):      # updates posts
    form_class = PostsForm
    model = Post
    template_name = 'post_edit.html'

    def get(self, request, *args, **kwargs):

        post = Post.objects.select_related('author').get(pk=self.kwargs['pk'])
        author = post.author

        # update only allowed if you are the creator
        if request.user == author:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class PostDelete(LoginRequiredMixin, DeleteView):      # deletes posts
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def get(self, request, *args, **kwargs):

        post = Post.objects.select_related('author').get(pk=self.kwargs['pk'])
        author = post.author

        # delete only allowed if you are the creator
        if request.user == author:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class PostsSelf(LoginRequiredMixin, ListView):                             # responsible for posts list with filters output
    model = Post
    ordering = '-time_in'
    template_name = 'posts_self.html'
    context_object_name = 'posts_self'
    paginate_by = 10

    def get_queryset(self):                            # redefine function to get posts list
        queryset = super().get_queryset()

        # save filtration in class object to reuse later, filer for posts by logged-in user
        self.filterset = PostsSelfFilter(self.request.GET, queryset.filter(author=self.request.user))

        return self.filterset.qs                       # return extended queryset

    def get_context_data(self, **kwargs):              # add filtration object to context and return extended context
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ReplyCreate(LoginRequiredMixin, CreateView):     # responsible for creating news
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_edit.html'

    # set creator as author
    def form_valid(self, form):
        reply = form.save(commit=False)

        # take author instance corresponding to the current user
        author = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])

        form.instance.author = author
        form.instance.post = post
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):

        post = Post.objects.select_related('author').get(pk=self.kwargs['pk'])
        author = post.author

        # replies only allowed on post of other authors
        if request.user != author:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('Вы не можете оставлять отклики на свои же посты')


class RepliesSelf(LoginRequiredMixin, ListView):       # responsible for posts list with filters output
    model = Reply
    ordering = '-time_in'
    template_name = 'replies_self.html'
    context_object_name = 'replies_self'
    paginate_by = 10

    def get_queryset(self):                            # redefine function to get posts list
        queryset = super().get_queryset()

        # save filtration in class object to reuse later, filer for posts by logged-in user
        self.filterset = ReplySelfFilter(self.request.GET, queryset.filter(author=self.request.user))

        return self.filterset.qs                       # return extended queryset

    def get_context_data(self, **kwargs):              # add filtration object to context and return extended context
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class RepliesOther(LoginRequiredMixin, ListView):       # responsible for posts list with filters output
    model = Reply
    ordering = '-time_in'
    template_name = 'replies_other.html'
    context_object_name = 'replies_other'
    paginate_by = 10

    def get_queryset(self):                            # redefine function to get posts list
        queryset = super().get_queryset()

        # save filtration in class object to reuse later, filer for posts by logged-in user
        self.filterset = ReplyOtherFilter(self.request.GET, queryset.filter(post__author=self.request.user))

        return self.filterset.qs                       # return extended queryset

    def get_context_data(self, **kwargs):              # add filtration object to context and return extended context
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
def accept_reply(request, pk):
    user = request.user
    reply = Reply.objects.get(pk=pk)

    # only receiver can accept reply
    if reply in Reply.objects.filter(post__author=user):

        if not reply.accepted:
            reply.accepted = True
            reply.save()

        # reload current page with parameters applied before
        path = re.sub(r'reply_\d*/accept', 'for_me_replies', request.get_full_path())
        return redirect(path)


@login_required
def delete_reply(request, pk):
    user = request.user
    reply = Reply.objects.get(pk=pk)

    # receiver or creator can delete replies
    if (receiver := reply in Reply.objects.filter(post__author=user)) \
            or (creator := reply in Reply.objects.filter(author=user)):
        reply.delete()

        # reload current page with parameters applied before
        if creator:
            path = re.sub(r'reply_\d*/delete', 'my_replies', request.get_full_path())

        elif receiver:
            path = re.sub(r'reply_\d*/delete', 'for_me_replies', request.get_full_path())

        return redirect(path)
