from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .models import Post


class PostListView(ListView):
    model = Post
    ordering = ['-data_postagem']
    context_object_name = 'posts'


class PostDetailView(DetailView):
    # DetailView já responde com 404 se o post não existir
    model = Post
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    fields = ['titulo', 'conteudo']


class PostUpdateView(UpdateView):
    model = Post
    fields = ['titulo', 'conteudo']


class PostDeleteView(DeleteView):
    # Template padrão: blog/post_confirm_delete.html (página de confirmação)
    model = Post
    success_url = reverse_lazy('post_list')
