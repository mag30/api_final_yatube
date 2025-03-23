from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, pagination, permissions, viewsets
from posts.models import Post, Group, Follow
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from .permissions import IsAuthorOrReadOnly


class PermissionViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(PermissionViewset):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(PermissionViewset):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.get_post_obj().comments.all()

    def get_post_obj(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_pk'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post_obj())


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)