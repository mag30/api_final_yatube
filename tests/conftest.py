# Импортируем необходимые модули
import sys  # Для работы с системными параметрами и путями
import os   # Для работы с файловой системой

# Определяем базовую директорию проекта.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Добавляем базовую директорию в пути поиска Python.
# Это необходимо для корректного импорта модулей из других частей проекта.
sys.path.append(BASE_DIR)

# Получаем список содержимого базовой директории.
root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = 'yatube_api'  # Ожидаемое имя папки с проектом

# Проверяем, что в базовой директории существует папка с проектом.
if (
        PROJECT_DIR_NAME not in root_dir_content
        or not os.path.isdir(os.path.join(BASE_DIR, PROJECT_DIR_NAME))
):
    assert False, (
        f'В директории `{BASE_DIR}` не найдена папка c проектом '
        f'`{PROJECT_DIR_NAME}`. Убедитесь, что у вас верная структура проекта.'
    )

# Формируем путь к директории проекта.
MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)

# Получаем список содержимого директории проекта.
project_dir_content = os.listdir(MANAGE_PATH)
FILENAME = 'manage.py'  # Ожидаемое имя файла для запуска Django-проекта

# Проверяем, что в директории проекта существует файл `manage.py`.
# Если его нет, вызываем ошибку с помощью assert.
if FILENAME not in project_dir_content:
    assert False, (
        f'В директории `{MANAGE_PATH}` не найден файл `{FILENAME}`. '
        'Убедитесь, что у вас верная структура проекта.'
    )

# Определяем список плагинов pytest для тестирования.
pytest_plugins = [
    'tests.fixtures.fixture_user',  # Фикстуры для работы с пользователями
    'tests.fixtures.fixture_data',  # Фикстуры для работы с данными
]

# Тестовый контент для README.md
default_md = '# api_final\napi final\n'
filename = 'README.md'  # Имя файла README

# Проверяем, что файл README.md существует в корне проекта.
# Если его нет, вызываем ошибку с помощью assert.
assert filename in root_dir_content, (
    f'В корне проекта не найден файл `{filename}.`'
)

# Открываем файл README.md для чтения.
with open(filename, 'r', errors='ignore') as f:
    file = f.read()  # Читаем содержимое файла

    # Проверяем, что содержимое файла README.md не совпадает с тестовым контентом.
    assert file != default_md, (
        f'Не забудьте оформить `{filename}.`'
    )