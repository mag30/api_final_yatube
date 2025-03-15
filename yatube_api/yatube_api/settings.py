from pathlib import Path
from datetime import timedelta

# Определяем базовую директорию проекта.
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ Django для шифрования и безопасности.
SECRET_KEY = 'hhz7l-ltdismtf@bzyz+rple7*s*w$jak%whj@(@u0eok^f9k4'

# Режим отладки. Если True, включаются дополнительные инструменты разработчика.
DEBUG = True

# Список хостов, которым разрешен доступ к приложению.
# В режиме DEBUG=True можно оставить пустым, но для production это необходимо настроить.
ALLOWED_HOSTS = []

# Список установленных приложений.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djoser',
    'api',
    'posts',
]

# Промежуточное ПО (Middleware) для обработки запросов.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Определяем основной модуль URL-конфигурации.
ROOT_URLCONF = 'yatube_api.urls'

# Настройка шаблонов.
TEMPLATES_DIR = BASE_DIR / 'templates'  # Директория с шаблонами
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Настройка WSGI-приложения.
WSGI_APPLICATION = 'yatube_api.wsgi.application'

# Настройка базы данных.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидаторы паролей для пользователей.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Проверка на схожесть с атрибутами пользователя
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Минимальная длина пароля
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Проверка на использование распространенных паролей
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Проверка на числовые пароли
    },
]

# Настройки локализации.
LANGUAGE_CODE = 'en-us'  # Язык по умолчанию
TIME_ZONE = 'UTC'  # Временная зона
USE_I18N = True  # Включение международизации
USE_L10N = True  # Локализация форматов даты и времени
USE_TZ = True  # Использование временной зоны

# Настройки статических файлов.
STATIC_URL = '/static/'  # URL для статических файлов
STATICFILES_DIRS = ((BASE_DIR / 'static/'),)  # Директории со статическими файлами

# Настройки Django REST Framework.
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # Разрешения: только чтение для неаутентифицированных пользователей
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Аутентификация через JWT
    ],
}

# Настройки Simple JWT (JSON Web Token).
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Время жизни токена доступа
    'AUTH_HEADER_TYPES': ('Bearer',),  # Тип аутентификации в заголовке
}

# Настройка автоматического поля для моделей.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'