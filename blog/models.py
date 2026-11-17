from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', blank=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nome


class Post(models.Model):
    titulo = models.CharField('Título', max_length=200)
    # O conteúdo é armazenado como código HTML e renderizado com o filtro safe.
    conteudo = models.TextField('Conteúdo (HTML)', help_text='Conteúdo da postagem em HTML')
    data_postagem = models.DateTimeField('Data de postagem', default=timezone.now)
    # Um post pode estar em várias categorias (e uma categoria tem vários posts)
    categories = models.ManyToManyField(Category, related_name='posts', blank=True,
                                        verbose_name='Categorias')

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        # Usado pelas CreateView/UpdateView para redirecionar após salvar
        return reverse('post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # Referência ao modelo User via settings.AUTH_USER_MODEL (conforme a documentação)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='comments')
    texto = models.TextField('Comentário')
    data_postagem = models.DateTimeField('Data de postagem', default=timezone.now)

    class Meta:
        # Mais recente primeiro
        ordering = ['-data_postagem']

    def __str__(self):
        return f'Comentário de {self.autor} em "{self.post}"'
