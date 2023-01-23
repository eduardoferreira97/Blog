# from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    # text = forms.CharField(widget=CKEditorWidget())

    class Meta:

        model = Post
        fields = ('title', 'text', 'slug', 'cover', 'author')
