from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from feed.models import Reply, Post


class IndexView(LoginRequiredMixin, ListView):                  # authorisation main view class
    queryset = Post.objects.all().order_by('-time_in')          # добавить get_queryset кастомный из вьюх NewsPaper и добавить пагинацию для reply
    template_name = 'authorisation/account.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):                           # modify context to know user's replies
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(post__author=self.request.user)
        return context

