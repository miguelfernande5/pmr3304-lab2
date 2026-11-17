"""Popula o banco com os dados pedidos na seção 4 do enunciado.

Uso (na raiz do projeto, com o ambiente virtual ativado):
    python manage.py migrate
    python popular_banco.py

Dados criados:
  - 4 usuários: admin (super-usuário), ana, bruno e carla
  - 3 categorias: Django, Python e SQL
  - 3 posts  (1 sem comentários; 2 com várias categorias)
  - 5 comentários (post 1 com 3 e post 2 com 2)
O script pode ser executado mais de uma vez: nada é duplicado.
"""
import os
from datetime import datetime, timezone as dt_timezone

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

from blog.models import Category, Comment, Post  # noqa: E402

User = get_user_model()


def utc(ano, mes, dia, hora, minuto):
    return datetime(ano, mes, dia, hora, minuto, 0, tzinfo=dt_timezone.utc)


# ------------------------------------------------------------------ usuários
senha_admin = os.environ.get('DJANGO_ADMIN_PASSWORD', 'admin12345')
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', senha_admin)

usuarios = {}
for nome, email in [('ana', 'ana@example.com'), ('bruno', 'bruno@example.com'),
                    ('carla', 'carla@example.com')]:
    usuarios[nome], _ = User.objects.get_or_create(username=nome, defaults={'email': email})
    if not usuarios[nome].has_usable_password():
        usuarios[nome].set_password('senha12345')
        usuarios[nome].save()

# ---------------------------------------------------------------- categorias
categorias = {}
for nome, descricao in [
    ('Django', 'Desenvolvimento web com o framework Django.'),
    ('Python', 'Linguagem de programação Python.'),
    ('SQL', 'Bancos de dados relacionais e consultas SQL.'),
]:
    categorias[nome], _ = Category.objects.get_or_create(
        nome=nome, defaults={'descricao': descricao})

# --------------------------------------------------------------------- posts
posts_dados = [
    {
        'titulo': 'Introdução ao Django',
        'data': utc(2026, 11, 2, 13, 0),
        'conteudo': (
            '<p>O <strong>Django</strong> é um framework web escrito em Python que '
            'segue o padrão MTV (Model, Template, View).</p>'
            '<p>Neste post vemos como criar um projeto, um app e o primeiro modelo.</p>'
            '<ul><li>django-admin startproject</li><li>python manage.py startapp</li>'
            '<li>python manage.py migrate</li></ul>'
        ),
        'categorias': ['Django', 'Python'],
        'comentarios': [
            ('ana', 'Ótima introdução! O padrão MTV ficou bem claro.', utc(2026, 11, 3, 10, 15)),
            ('bruno', 'Faltou falar sobre o painel de administração.', utc(2026, 11, 3, 18, 40)),
            ('carla', 'Vou usar este roteiro para o meu laboratório.', utc(2026, 11, 4, 9, 5)),
        ],
    },
    {
        'titulo': 'Consultas SQL com JOIN',
        'data': utc(2026, 11, 9, 15, 30),
        'conteudo': (
            '<p>O <em>JOIN</em> combina linhas de duas ou mais tabelas a partir de uma '
            'coluna relacionada.</p>'
            '<pre>SELECT * FROM blog_post p JOIN blog_comment c ON c.post_id = p.id;</pre>'
            '<p>Também vemos <code>GROUP BY</code> e <code>HAVING</code>.</p>'
        ),
        'categorias': ['SQL', 'Django'],
        'comentarios': [
            ('bruno', 'O exemplo com GROUP BY ajudou bastante.', utc(2026, 11, 10, 11, 20)),
            ('ana', 'Dá para fazer o mesmo pelo ORM do Django?', utc(2026, 11, 11, 8, 50)),
        ],
    },
    {
        'titulo': 'Dicas de Python para iniciantes',
        'data': utc(2026, 11, 13, 17, 45),
        'conteudo': (
            '<p>Algumas dicas para quem está começando em <strong>Python</strong>:</p>'
            '<ol><li>Use ambientes virtuais.</li><li>Leia a documentação oficial.</li>'
            '<li>Pratique com projetos pequenos.</li></ol>'
        ),
        'categorias': ['Python'],
        'comentarios': [],  # este post fica sem comentários
    },
]

for dados in posts_dados:
    post, criado = Post.objects.get_or_create(
        titulo=dados['titulo'],
        defaults={'conteudo': dados['conteudo'], 'data_postagem': dados['data']},
    )
    if criado:
        post.categories.set([categorias[n] for n in dados['categorias']])
        for autor, texto, data in dados['comentarios']:
            Comment.objects.create(post=post, autor=usuarios[autor], texto=texto,
                                   data_postagem=data)

print(f'Usuários:    {User.objects.count()}')
print(f'Categorias:  {Category.objects.count()}')
print(f'Posts:       {Post.objects.count()}')
print(f'Comentários: {Comment.objects.count()}')
