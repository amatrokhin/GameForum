from django.urls import path
from .views import IndexView
from feed.views import accept_reply, delete_reply, PostsSelf, RepliesSelf, RepliesOther

urlpatterns = [
    path('personal/', IndexView.as_view(), name='personal_space'),
    path('personal/reply_<int:pk>/accept/', accept_reply, name='accept_reply'),
    path('personal/reply_<int:pk>/delete/', delete_reply, name='delete_reply'),
    path('personal/my_posts/', PostsSelf.as_view(), name='posts_self'),
    path('personal/my_replies/', RepliesSelf.as_view(), name='replies_self'),
    path('personal/for_me_replies/', RepliesOther.as_view(), name='replies_other'),
]
