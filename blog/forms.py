from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo']
        labels = {'titulo': 'Título', 'conteudo': 'Conteúdo (HTML)'}
        widgets = {'conteudo': forms.Textarea(attrs={'rows': 12, 'cols': 70})}
