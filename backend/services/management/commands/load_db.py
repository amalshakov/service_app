import json
import os

from clients.models import Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from services.models import Plan, Service, Subscription

User = get_user_model()


def process_file(name: str):
    with open(
        os.path.join(settings.BASE_DIR, "data/", name),
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


class Command(BaseCommand):

    def handle(self, *args, **options):

        data = process_file("users.json")
        for email, value in data.items():
            User.objects.create(
                email=email,
                password=value[0],
                first_name=value[1],
                last_name=value[2],
                username=value[3],
            )
        print("----- Пользователи загружены! (User) -----")

        data = process_file("clients.json")
        for company_name, value in data.items():
            Client.objects.create(
                company_name=company_name,
                user=User.objects.get(id=value[0]),
                full_address=value[1],
            )
        print("----- Клиенты загружены! (Client) -----")

        data = process_file("services.json")
        for name, value in data.items():
            Service.objects.create(
                name=name,
                full_price=value[0],
            )
        print("----- Услуги загружены! (Service) -----")

        data = process_file("plans.json")
        for plan_type, value in data.items():
            Plan.objects.create(
                plan_type=plan_type,
                discount_percent=value[0],
            )
        print("----- тарифные Планы загружены! (Plan) -----")

        data = process_file("subscriptions.json")
        for comment, value in data.items():
            Subscription.objects.create(
                comment=comment,
                client=Client.objects.get(id=value[0]),
                service=Service.objects.get(id=value[1]),
                plan=Plan.objects.get(id=value[2]),
            )
        print("----- Подписки загружены! (Subscription) -----")
