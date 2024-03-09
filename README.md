# Проект создан исключительно:
- для опыта оптимизации Django:
    - оптимизация ORM-query
    - annotate и aggregate
    - cellery, SingleTone, решение проблем параллельных cellery tasks
    - redis и ручной кэш
    - DB index
    - django-cachalot (глобальное кэширование)

# Основные технологии:
- celery[redis]==5.2.7
- celery_singleton==0.3.1
- django-redis==5.2.0
- flower==1.2.0
- django-cachalot==2.6.2
- Django==3.2.16
- djangorestframework==3.14.0

# Запуск проекта
```
git clone git@github.com:amalshakov/service_app.git
docker-compose up --build
docker-compose run --rm backend-app sh -c "python manage.py makemigrations"
docker-compose run --rm backend-app sh -c "python manage.py migrate"
docker-compose run --rm backend-app sh -c "python manage.py load_db"
docker-compose run --rm backend-app sh -c "python manage.py createsuperuser"
```

# Главная модель Subscription:
 - содержит поля:
    - client (FK на клиента, который оформляет подписку)
    - service (FK на услугу, на которую подписывается клиент)
    - plan (FK на тарифный план, по которому подписывается клиент)
    - price (итоговая цена, считается автоматически)

# Основные URL:
- Flower
    - http://127.0.0.1:5555/
- Админка
    - http://127.0.0.1:8000/admin/
- Подписки
    - http://127.0.0.1:8000/api/subscriptions/

# Дополнительно:
- .env выложен в Git. каюсь...

СДЕЛАЙ ВЕРНУЮ СОРТИРОВКУ!!!!!