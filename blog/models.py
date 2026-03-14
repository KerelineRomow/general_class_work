from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Назва")
    slug = models.SlugField(max_length=220, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Тег")
    slug = models.SlugField(max_length=220, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"





class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name= "Заголовок")
    content = models.TextField(verbose_name= "Опис")
    published_date = models.DateTimeField(auto_created=True, verbose_name= "Дата публикации")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name= "Категория")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name= "Автор")
    image = (models.URLField
             (default="https://marketplace.canva.com/EAGtrPC4Xiw/1/0/1600w/canva-black-and-white-artistic-woman-portrait-instagram-profile-picture-dUziP3tUikw.jpg"))
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    tags = models.ManyToManyField(Tag,blank=True, related_name="tags", verbose_name="Теги")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новина"
        verbose_name_plural = "Новини"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")

    author = models.CharField(max_length=50, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст коментаря")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"{self.author} - {self.post.title}"

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"

