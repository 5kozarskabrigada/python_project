from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'title', 'content', 'image', 'is_draft']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15}),
        }