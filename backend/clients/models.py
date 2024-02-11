from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CLient(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=100)
    full_address = models.CharField(max_length=100)
