from django import forms
from django.core.exceptions import ValidationError
from ckeditor import widgets

from .models import Post, Reply


class PostsForm(forms.ModelForm):                    # responsible for form to create news

    title = forms.CharField(
        widget=forms.Textarea(attrs={
            'required': True,                       # To notify creator to fill the field
            'placeholder': 'Ваш заголовок тут',
            'cols': 120,
            'rows': 1,
        })
    )

    content = forms.CharField(
        min_length=20,
        required=True,
        widget=widgets.CKEditorWidget()
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
        ]

    def clean(self):                                # validation of input data
        cleaned_data = super().clean()

        content = cleaned_data.get("content")
        title = cleaned_data.get("title")

        if title == content:
            raise ValidationError(
                "Заголовок и текст статьи не должны совпадать."
            )

        return cleaned_data


class ReplyForm(forms.ModelForm):

    text = forms.CharField(
        min_length=20,
        widget=forms.Textarea(attrs={
            'required': True,
            'placeholder': 'Ваш текст здесь',
            'cols': 160,
        })
    )

    class Meta:
        model = Reply
        fields = ['text', ]
