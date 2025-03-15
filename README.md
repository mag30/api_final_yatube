# Проект API для Yatube
Проект в виде социальной сети с публикациями, комментариями, группами и подписками.

# Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/mag30/api_final_yatube.git
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
