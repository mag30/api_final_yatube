from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import permissions

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='posts',
        null=True, blank=True)

    class Meta:
        ordering = ['-pub_date']  # Сортировка по убыванию даты публикации

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']  # Сортировка по убыванию даты создания комментария

    def __str__(self):
        return self.text[:15]  # Выводим первые 15 символов текста


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='prevent_self_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} follows {self.following}'


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет:
    - Безопасные методы (GET, HEAD, OPTIONS) всем пользователям.
    - Модификацию объектов только их авторам.
    """

    def has_permission(self, request, view):
        # Разрешаем доступ для безопасных методов
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ для безопасных методов
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем модификацию только автору объекта
        return obj.author == request.user