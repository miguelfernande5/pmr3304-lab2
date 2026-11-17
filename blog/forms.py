from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo']
        labels = {'titulo': 'Título', 'conteudo': 'Conteúdo (HTML)'}
        widgets = {'conteudo': forms.Textarea(attrs={'rows': 12, 'cols': 70})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['texto']
        labels = {'texto': 'Comentário'}
        widgets = {'texto': forms.Textarea(attrs={'rows': 4, 'cols': 70})}
