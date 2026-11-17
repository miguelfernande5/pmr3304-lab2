from django.shortcuts import get_object_or_404, redirect, render

from .models import Post


def post_list(request):
    posts = Post.objects.order_by('-data_postagem')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    # get_object_or_404 responde com 404 se o post não existir
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_create(request):
    if request.method == 'POST':
        # Sem Django forms e sem validação: lê direto de request.POST
        post = Post.objects.create(
            titulo=request.POST['titulo'],
            conteudo=request.POST['conteudo'],
        )
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html')


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.titulo = request.POST['titulo']
        post.conteudo = request.POST['conteudo']
        post.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'post': post})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    # GET: página de confirmação de remoção
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
