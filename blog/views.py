from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import CommentForm
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
    model = Post
    success_url = reverse_lazy('post_list')


@login_required
def comment_create(request, pk):
    """Cria um comentário no post `pk`. O autor é o usuário logado."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.autor = request.user
            comentario.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})
