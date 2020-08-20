from django import forms
from article.models import Article


class ArticleForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=128)
    content = forms.CharField(label='Content', widget=forms.Textarea)
    
    
    class Meta:
        model = Article
        fields = ['title', 'content']