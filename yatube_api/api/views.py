from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, pagination, permissions, viewsets
from posts.models import Post, Group, Follow
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from .permissions import OwnershipPermission  # Пользовательские разрешения


# Базовый ViewSet с настройкой разрешений.
class PermissionViewset(viewsets.ModelViewSet):
    # Устанавливаем разрешение OwnershipPermission для всех наследников этого класса.
    permission_classes = (OwnershipPermission,)


# ViewSet для модели Group (только чтение).
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    # Определяем набор данных (все группы).
    queryset = Group.objects.all()
    # Указываем сериализатор для преобразования данных.
    serializer_class = GroupSerializer


# ViewSet для модели Post.
class PostViewSet(PermissionViewset):
    # Определяем набор данных (все посты).
    queryset = Post.objects.all()
    # Указываем сериализатор для преобразования данных.
    serializer_class = PostSerializer
    # Настройка пагинации: используем LimitOffsetPagination.
    pagination_class = pagination.LimitOffsetPagination

    # Переопределяем метод perform_create для сохранения автора поста.
    def perform_create(self, serializer):
        # Сохраняем пост, автоматически устанавливая автора как текущего пользователя.
        return serializer.save(
            author=self.request.user
        )


# ViewSet для модели Comment.
class CommentViewSet(PermissionViewset):
    # Определяем сериализатор для преобразования данных.
    serializer_class = CommentSerializer

    # Переопределяем метод get_queryset для фильтрации комментариев по конкретному посту.
    def get_queryset(self):
        # Возвращаем все комментарии, связанные с конкретным постом.
        return self.get_post_obj().comments.all()

    # Вспомогательный метод для получения объекта Post.
    def get_post_obj(self):
        # Получаем объект Post по его ID из URL-параметров (post_pk).
        # Если объект не найден, возвращается ошибка 404.
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('post_pk')
        )

    # Переопределяем метод perform_create для сохранения автора комментария и связи с постом.
    def perform_create(self, serializer):
        # Сохраняем комментарий, автоматически устанавливая автора и связь с постом.
        return serializer.save(
            author=self.request.user,
            post=self.get_post_obj()
        )


# ViewSet для модели Follow (подписки).
class FollowViewSet(
    viewsets.GenericViewSet,  # Базовый класс для создания собственных ViewSet
    mixins.CreateModelMixin,  # Поддержка создания объектов
    mixins.ListModelMixin  # Поддержка списка объектов
):
    # Определяем набор данных (все подписки).
    queryset = Follow.objects.all()
    # Указываем сериализатор для преобразования данных.
    serializer_class = FollowSerializer
    # Разрешения: только аутентифицированные пользователи могут взаимодействовать с подписками.
    permission_classes = (permissions.IsAuthenticated,)
    # Настройка фильтрации: поиск по имени пользователя (following__username).
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    # Переопределяем метод get_queryset для фильтрации подписок текущего пользователя.
    def get_queryset(self):
        # Возвращаем все подписки текущего пользователя.
        return self.request.user.follower.all()

    # Переопределяем метод perform_create для сохранения подписчика.
    def perform_create(self, serializer):
        # Сохраняем подписку, автоматически устанавливая подписчика как текущего пользователя.
        serializer.save(user=self.request.user)