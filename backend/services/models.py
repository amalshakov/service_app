from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_delete

from clients.models import Client
from services.signals import delete_cache_total_sum
from services.tasks import set_comment, set_price


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs) -> None:
        if self.full_price != self.__full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class Plan(models.Model):
    PLAN_TYPES = (
        ("full", "Full"),
        ("student", "Student"),
        ("discount", "Discount"),
    )
    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs) -> None:
        if self.discount_percent != self.__discount_percent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.plan_type}"


class Subscription(models.Model):
    client = models.ForeignKey(
        Client, related_name="subscriptions", on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        Service, related_name="subscriptions", on_delete=models.CASCADE
    )
    plan = models.ForeignKey(
        Plan, related_name="subscriptions", on_delete=models.CASCADE
    )
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=50, default="default", db_index=True)
    comment_a = models.CharField(max_length=50, default="default")
    comment_b = models.CharField(max_length=50, default="default")

    def __str__(self) -> str:
        return f"{self.client} - {self.service} - {self.plan}"

    class Meta:
        ordering = ("id",)
        indexes = [models.Index(fields=["comment_a", "comment_b"])]

    def save(self, *args, **kwargs) -> None:
        creating = not bool(self.id)
        result = super().save(*args, **kwargs)
        if creating:
            set_price.delay(self.id)
        return result


post_delete.connect(delete_cache_total_sum, sender=Subscription)
