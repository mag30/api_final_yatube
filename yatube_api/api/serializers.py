from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField
from posts.models import Comment, Post, Group, Follow


# Сериализатор для модели Post.
class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        # Указываем, что все поля модели Post будут сериализованы.
        fields = '__all__'
        model = Post  # Связываем сериализатор с моделью Post.


# Сериализатор для модели Comment.
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        # Указываем, что все поля модели Comment будут сериализованы.
        fields = '__all__'
        # Поле post доступно только для чтения, чтобы предотвратить изменение через API.
        read_only_fields = ('post',)
        model = Comment  # Связываем сериализатор с моделью Comment.


# Сериализатор для модели Group.
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group  # Связываем сериализатор с моделью Group.
        # Указываем поля, которые будут сериализованы.
        fields = ('id', 'title', 'slug', 'description')
        # Все поля доступны только для чтения, чтобы предотвратить изменение через API.
        read_only_fields = ('id', 'title', 'slug', 'description')


# Сериализатор для модели Follow (подписки).
class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all(),
        default=serializers.CurrentUserDefault()
    )
    # Поле following также представлено как SlugRelatedField для отображения username автора.
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Follow  # Связываем сериализатор с моделью Follow.
        fields = ('user', 'following')  # Указываем поля, которые будут сериализованы.
        # Добавляем валидатор, который проверяет уникальность пары (user, following).
        validators = (
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=('Подписка уже существует')
            ),
        )

    # Метод validate выполняет дополнительные проверки данных перед сохранением.
    def validate(self, data):
        # Проверяем, что пользователь не пытается подписаться на самого себя.
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Попытка подписаться на себя же'
            )
        return data