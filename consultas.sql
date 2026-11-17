-- ===========================================================================
-- Seção 4 - Exercícios com SQL (banco db.sqlite3)
-- Tabelas criadas pelo Django: blog_post, blog_comment, blog_category e
-- blog_post_categories (tabela intermediária do ManyToMany).
-- ===========================================================================

-- 1. Todos os posts, ordenados pela data, mais recente primeiro
SELECT *
FROM blog_post
ORDER BY data_postagem DESC;

-- 2. Para um post com comentários (post de id = 1), todos os seus comentários
SELECT *
FROM blog_comment
WHERE post_id = 1;

-- 3. Comentários do post 1, com todas as colunas da tabela de comentários
--    (exceto post_id), o título do post e a data de publicação como post_date
SELECT c.id,
       c.autor_id,
       c.texto,
       c.data_postagem,
       p.titulo,
       p.data_postagem AS post_date
FROM blog_comment AS c
JOIN blog_post AS p ON p.id = c.post_id
WHERE p.id = 1;

-- 4. Para uma categoria (id = 1, "Django"), todos os posts pertencentes a ela,
--    com as colunas da tabela de categoria e da tabela de posts
SELECT cat.id   AS categoria_id,
       cat.nome,
       cat.descricao,
       p.id     AS post_id,
       p.titulo,
       p.conteudo,
       p.data_postagem
FROM blog_category AS cat
JOIN blog_post_categories AS pc ON pc.category_id = cat.id
JOIN blog_post AS p ON p.id = pc.post_id
WHERE cat.id = 1;

-- 5. Todas as categorias que possuem dois ou mais posts
SELECT cat.id,
       cat.nome,
       cat.descricao,
       COUNT(pc.post_id) AS total_posts
FROM blog_category AS cat
JOIN blog_post_categories AS pc ON pc.category_id = cat.id
GROUP BY cat.id, cat.nome, cat.descricao
HAVING COUNT(pc.post_id) >= 2;
