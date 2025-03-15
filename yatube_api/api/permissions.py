from rest_framework import permissions


# Создаем пользовательский класс разрешений, наследуясь от BasePermission.
class OwnershipPermission(permissions.BasePermission):

    # Метод has_permission определяет, есть ли у пользователя право выполнять запрос на уровне всего представления (view).
    def has_permission(self, request, view):
        return (
            # Разрешаем доступ, если метод запроса является "безопасным"
            request.method in permissions.SAFE_METHODS
            # Или если пользователь аутентифицирован (залогинен).
            or request.user.is_authenticated
        )

    # Метод has_object_permission определяет, есть ли у пользователя право выполнять запрос на уровне конкретного объекта (obj).
    def has_object_permission(self, request, view, obj):
        return (
            # Разрешаем доступ, если метод запроса является "безопасным".
            request.method in permissions.SAFE_METHODS
            # Или если автор объекта совпадает с текущим пользователем.
            or obj.author == request.user
        )