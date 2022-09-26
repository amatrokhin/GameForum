from django.db import models
from django.contrib.auth.models import User
from ckeditor import fields
from django.urls import reverse


CATEGORIES = (
    ('ТН', 'Танки'),
    ('ХЛ', 'Хилы'),
    ('ДД', 'ДД'),
    ('ТГ', 'Торговцы'),
    ('ГМ', 'Гилдмастеры'),
    ('КГ', 'Квестгиверы'),
    ('КЗ', 'Кузнецы'),
    ('КЖ', 'Кожевники'),
    ('ЗВ', 'Зельевары'),
    ('МЗ', 'Мастера заклинаний'),
)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = fields.RichTextField()            # allows pictures and video in text
    time_in = models.DateTimeField(auto_now_add=True)

    category = models.CharField(max_length=2, choices=CATEGORIES, default='Тн')

    def preview(self):
        return self.content[:124] + '...'

    def get_absolute_url(self):                 # this allows us to go to the post page after creating a post
        return reverse('post_detail', args=[str(self.id)])


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def preview(self):
        return self.text[:124] + '...'

    def get_absolute_url(self):                 # this allows us to go to the post page after creating a post
        return reverse('post_detail', args=[str(self.post.id)])
