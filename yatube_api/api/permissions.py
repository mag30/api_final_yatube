from rest_framework import permissions


# Создаем пользовательский класс разрешений, наследуясь от BasePermission.
class IsAuthorOrReadOnly(permissions.BasePermission):

    # Метод has_permission определяет, есть ли у пользователя право выполнять запрос на уровне всего представления (view).
    def has_permission(self, request, view):
        # Разрешаем доступ для безопасных методов
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ для безопасных методов
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем модификацию только автору объекта
        return obj.author == request.user