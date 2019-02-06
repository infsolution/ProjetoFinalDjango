from django import forms
from django.forms import ModelForm
from posts.models import *


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postagem']
        widgets = {
            'postagem': forms.Textarea(attrs={'class': 'form-control', 'maxlength': 255, 'rows': '4', 'cols': '20'}),
        }

